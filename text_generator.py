#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, re, time, base64
import requests
from openpyxl import Workbook

API_URL = "https://api.xi-ai.cn/v1/chat/completions"
API_KEY = os.getenv("API_KEY")

CHINESE_MODELS = ["deepseek-v3", "qwen3-max"]
ENGLISH_MODELS = ["gpt-5.1", "claude-opus-4", "gemini-3-pro-thinking", "grok-4.1"]
ALL_MODELS = CHINESE_MODELS + ENGLISH_MODELS

PROMPT_FILE = "data/text/text_prompt.txt"
IMAGE_BASE_DIR = "data/text"
OUTPUT_FILE = "output/text/text_output.xlsx"


def read_tasks(path: str):
    """
    解析格式:
      T-5:5.jpg
      <中文>

      <英文>

    image 可省略。
    """
    text = open(path, "r", encoding="utf-8").read()
    pattern = r"(T-[^:]+:[^\n]*\n)(.*?)(?=(?:T-[^:]+:[^\n]*\n)|$)"
    tasks = {}

    for header, body in re.findall(pattern, text, re.DOTALL):
        header = header.strip()  # e.g. "T-5:5.jpg"
        body = body.strip()

        # task id
        m = re.search(r"\d+", header)
        task_id = int(m.group()) if m else (len(tasks) + 1)

        # image file
        image_file = None
        if ":" in header:
            maybe = header.split(":", 1)[1].strip()
            if maybe.lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
                image_file = maybe

        parts = [p.strip() for p in body.split("\n\n") if p.strip()]
        zh = parts[0] if parts else body
        en = parts[1] if len(parts) > 1 else zh

        tasks[task_id] = {
            "full": f"{header}\n{body}",
            "zh": zh,
            "en": en,
            "image": image_file,
        }

    return tasks


def image_to_data_url(image_file: str):
    if not image_file:
        return None
    p = os.path.join(IMAGE_BASE_DIR, image_file)
    if not os.path.exists(p):
        return None
    data = open(p, "rb").read()
    b64 = base64.b64encode(data).decode("utf-8")
    ext = os.path.splitext(image_file.lower())[1]
    mime = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
    }.get(ext, "image/jpeg")
    return f"data:{mime};base64,{b64}"


def call_model(model: str, prompt: str, image_file: str | None, retries=2, timeout=60):
    if not API_KEY:
        raise RuntimeError("缺少环境变量 API_KEY")

    data_url = image_to_data_url(image_file) if image_file else None
    content = f"{data_url}\n\n{prompt}" if data_url else prompt

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content}],
        "temperature": 0.7,
        "max_tokens": 2000,
        "top_p": 0.9,
        "stream": False,
    }
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}

    last_err = None
    for _ in range(retries + 1):
        try:
            r = requests.post(API_URL, headers=headers, json=payload, timeout=timeout)
            if r.status_code != 200:
                last_err = f"HTTP {r.status_code}"
                time.sleep(2)
                continue
            j = r.json()
            return j["choices"][0]["message"]["content"].strip()
        except Exception as e:
            last_err = str(e)
            time.sleep(2)

    return f"错误: {last_err or 'unknown'}"


def save_xlsx(tasks, results, out_path: str):
    wb = Workbook()
    ws = wb.active
    ws.title = "Sheet1"

    ws.append(["prompt"] + ALL_MODELS)
    for tid in sorted(tasks):
        row = [tasks[tid]["full"]]
        for m in ALL_MODELS:
            row.append(results.get(tid, {}).get(m, ""))
        ws.append(row)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    wb.save(out_path)


def main():
    tasks = read_tasks(PROMPT_FILE)
    results = {}

    for tid in sorted(tasks):
        print(f"正在处理 T-{tid}...")
        t = tasks[tid]
        results[tid] = {}
        # 中文模型跑中文 prompt；英文模型跑英文 prompt（都可带同一张图）
        for m in CHINESE_MODELS:
            results[tid][m] = call_model(m, t["zh"], t["image"])
        for m in ENGLISH_MODELS:
            results[tid][m] = call_model(m, t["en"], t["image"])

    save_xlsx(tasks, results, OUTPUT_FILE)
    print(f"saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
