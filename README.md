# PaperSearch 📄🔍

PaperSearch is a Python tool that automates the process of finding and screening research papers from Arxiv. By leveraging Large Language Models (LLMs) like **OpenAI**, **GitHub Copilot (GitHub Models)**, or **DeepSeek**, it intelligently filters papers based on your custom criteria, saving you hours of manual searching.

## ✨ Features

- **Smart Search**: Search Arxiv using keywords with options to sort by **Relevance** or **Submission Date**.
- **Time Filtering**: Option to filter out older papers when searching by relevance (e.g., "only papers from 2024 onwards").
- **AI Screening**: Uses LLMs to read paper titles and abstracts against your specific criteria (e.g., "Must focus on transformer architecture").
- **Flexible Configuration**: Fully interactive CLI to control search depth, target paper count, and screening rules.
- **Model Agnostic**: Compatible with any OpenAI-API-compatible provider:
  - DeepSeek (Recommended for cost/performance)
  - GitHub Models (Copilot)
  - OpenAI (GPT-4o, GPT-3.5)
  - Local LLMs (Ollama, LM Studio)
- **Report Generation**: Automatically generates a clean Markdown report (`accepted_papers.md`) with summaries, links, and AI reasoning.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- An API Key for your chosen LLM provider (OpenAI, GitHub, DeepSeek, etc.)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/wandering-tiger/PaperSearch.git
   cd PaperSearch
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   Rename `.env.example` to `.env` and configure your API key.

   ```bash
   mv .env.example .env
   ```

   **Example `.env` configurations:**

   *Option 1: OpenAI Official (Recommended)*
   ```properties
   OPENAI_BASE_URL=https://api.openai.com/v1
   OPENAI_API_KEY=sk-your-openai-key
   MODEL_NAME=gpt-5.4
   ```

   *Option 2: DeepSeek*
   ```properties
   OPENAI_BASE_URL=https://api.deepseek.com
   OPENAI_API_KEY=sk-your-deepseek-key
   MODEL_NAME=deepseek-chat
   ```

   *Option 3: GitHub Models (Copilot)*
   ```properties
   OPENAI_BASE_URL=https://models.inference.ai.azure.com
   OPENAI_API_KEY=github_pat_xxxx
   MODEL_NAME=gpt-4o
   ```


## 📖 Usage

Run the main script:

```bash
python src/main.py
```

The tool will guide you through an interactive process:

1.  **Enter Keywords**: e.g., "Large Language Models Survey".
2.  **Set Criteria**: e.g., "Focus on reasoning capabilities and chain-of-thought."
3.  **Choose Sorting**: Sort by Relevance or Date.
4.  **Set Filters**: (Optional) Filter out papers before a certain year.
5.  **Set Limits**: Decide how many papers to scan from Arxiv (e.g., 50) and how many approved papers you want (e.g., 10).

### Output

The script generates a file named `accepted_papers.md` in the current directory.

**Example Report:**
```markdown
# Paper Search Report
Date: 2024-03-12 10:00:00

## 1. A Survey of Large Language Models
**Authors:** Wayne Xin Zhao, ...
**Published:** 2023-03-31
**Link:** [PDF](http://arxiv.org/pdf/2303.18223v2)
**Summary:** ...
**AI Evaluation:** 
Decision: ACCEPT
Reasoning: This paper provides a comprehensive review of the development of LLMs...
```

## 🛠 Project Structure

- `src/main.py`: Main entry point and interactive logic.
- `src/arxiv_client.py`: Handles communication with Arxiv API.
- `src/llm_client.py`: Unified client for calling LLM APIs (OpenAI/DeepSeek/Copilot).
- `requirements.txt`: Python dependencies.

## 📄 License

[MIT](LICENSE)
