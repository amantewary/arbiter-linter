# Arbiter: LLM Prompt Interference Linter ⚖️

[![GitHub Action](https://img.shields.io/badge/GitHub-Action-blue?logo=github)](https://github.com/marketplace/actions/arbiter-prompt-linter)

Arbiter is a specialized auditor for LLM system prompts. It uses an LLM 'Scourer' to detect logical conflicts, redundancies, and interference patterns that confuse autonomous agents.

Inspired by the research paper: [*"Arbiter: Detecting Interference in LLM Agent System Prompts"* (Tony Mason, 2026)](http://arxiv.org/abs/2603.08993v1).

## 💡 Why Arbiter?

System prompts for coding agents are software artifacts. As they grow in complexity, rules often "interfere" with each other—causing agents to ignore instructions, hallucinate, or fail silently. Arbiter treats prompts as code and applies automated linting to find these bugs before they hit production.

### What it detects:
- **Conflict:** Direct contradictions between rules (e.g., 'be concise' vs 'be verbose').
- **Shadowing:** Broad rules that make specific rules unreachable.
- **Redundancy:** Rules stated multiple times, wasting tokens and confusing attention.
- **Ambiguity:** Phrasing that allows dangerous or unpredictable interpretations.

---

## 🛠 Usage

### 1. As a GitHub Action (Recommended)

Add this workflow to your repository (e.g., `.github/workflows/lint-prompts.yml`):

```yaml
name: Lint System Prompts

on:
  push:
    paths:
      - 'prompts/**'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Arbiter
        uses: amantewary/arbiter-linter@v1
        with:
          directory: './prompts'
          gemini_api_key: ${{ secrets.GEMINI_API_KEY }}
```

### 2. As a CLI Tool

```bash
# Clone and install dependencies
pip install google-genai

# Run the linter
python arbiter.py ./your-prompts-folder --key YOUR_GEMINI_KEY
```

---

## ⚙️ Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `directory` | Yes | `.` | Folder containing your `.md` prompt files. |
| `gemini_api_key` | Yes | | Your Gemini API Key. |
| `model` | No | `gemini-2.5-flash` | The auditor model to use. |

## 🚀 Deployment Strategy

1. **Local Development:** Developers use the CLI tool to check for conflicts while drafting new rules.
2. **CI/CD Integration:** The GitHub Action runs on every PR, ensuring no conflicting rules are merged into the main prompt set.
3. **Multi-Model Scouring:** (Advanced) Run Arbiter using different models (e.g., Claude vs GPT) to find different classes of interference.
