# GenAI Value Safety Benchmark (GVS-Bench)

This is the official repository of **"Seeking Human Security Consensus: A Unified Value Scale for Generative AI Value Safety."**
It provides the **data and evaluation guidelines** for the **GenAI Value Safety Benchmark (GVS-Bench)**.

⚠️ **Usage Notice**
The benchmark is released **for academic research and evaluation purposes only** and **must not be misused**.

---

## Overview

**GenAI Value Safety Benchmark (GVS-Bench)** is constructed to operationalize and validate the proposed **GenAI Value Safety Scale (GVS-Scale)**.

GVS-Bench translates abstract value safety dimensions into **concrete, reproducible evaluation tasks**, enabling systematic assessment of generative AI models from a value safety perspective.

---

## Construction of GVS-Bench

GVS-Bench is built directly upon the **GVS-Scale**, which defines a unified value safety framework with:

- **3 layers**
- **12 value categories**

### Benchmark Design

- **Category-driven construction**
  Evaluation tasks are designed according to the **12 value categories** defined in the GVS-Scale.
- **Incident-grounded prompts**
  Test cases are derived from real-world value safety incidents or their abstracted variants,
  ensuring realistic and meaningful evaluation scenarios.
- **Modality-specific evaluation**Rather than assuming identical risk expressions, GVS-Bench explicitly distinguishes between
  different generative modalities:

  - Text
  - Image
  - Video
  - Audio

  Prompts are tailored to each modality while preserving a **consistent value-level evaluation target**.

---

## GVS-Bench Dataset

### GVS-Bench.xlsx

`GVS-Bench.xlsx` contains the complete benchmark test set.

**Structure:**The dataset is organized as a **two-dimensional table** based on the **GVS-Scale**, covering:

- **12 value categories**
- **4 generative AI modalities** (Text, Image, Video, Audio)

This structure ensures comprehensive and balanced coverage of GenAI value safety risks.

---

## Evaluation Pipeline (LLM-as-a-Judge)

This repository provides a reference implementation of an **LLM-as-a-judge** evaluation pipeline.

### 1. Text Generation (`text_generator.py`)

**Purpose:**
Generate model responses for GVS-Bench test cases.

**Generation Models:**

- GPT-5.1
- Claude Opus 4
- Gemini 3 Pro
- Grok 4.1
- Qwen3
- DeepSeek-v3

**Behavior:**

- Iterates over all benchmark test cases
- Generates one response per model per test case
- Reports generation status in terminal:
  ```
  正在处理 T-x...
    [i/6] <model_name>: 成功 / 失败(reason)
  ```

**Output:**

```
output/text/text_output.xlsx
```

---

### 2. Value Safety Scoring (`llm_rate.py`)

**Purpose:**
Evaluate generated responses using a stronger LLM as a judge.

**Judge Model:**

- **GPT-5.2**

**Behavior:**

- Loads generated answers
- Scores each response according to GVS-Scale-aligned criteria
- Reports success or failure for each scoring task:
  ```
  正在处理 T-x...
    [i/6] <generation_task>: 成功(score) / 失败(reason)
  ```

**Judge Output Format:**

```
Score: x/10
Brief reason: ...
```

**Output:**

```
rate/text_rate.xlsx
```

---

## Design Principles

- **Value-scale grounded**
  All evaluation tasks are aligned with the GVS-Scale.
- **Modality-aware**
  Value safety risks are assessed in modality-specific contexts.
- **Scalable evaluation**
  The LLM-as-a-judge paradigm enables consistent and reproducible scoring.

---

## Requirements

- Python 3.9+
- `requests`
- `pandas`
- `openpyxl`

Install dependencies:

```bash
pip install requests pandas openpyxl
```

---

## Environment Variables

```bash
export API_KEY="your_api_key_here"
```

---

## Running the Evaluation

```bash
python text_generator.py
python llm_rate.py
```

---

## License & Usage

This benchmark is released **for academic research and evaluation purposes only**.
Any misuse, including generating or amplifying harmful content, is strictly prohibited.
