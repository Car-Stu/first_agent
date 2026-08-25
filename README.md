# Local AI Assistant with LLMops Tracing

A lightweight, production-grade AI agent infrastructure utilizing free, open-source models and automated telemetry tracking.

## Architecture & Infrastructure
- **LLM Engine:** Serverless inference using `Qwen/Qwen2.5-Coder-7B-Instruct`
- **Observability (LLMops):** Automated trace logging and latency metrics via **Opik**
- **Environment Management:** Strict type and secret sandboxing using `.env` validation

## Getting Started

### Prerequisites
- Python 3.10+
- A Hugging Face account and Access Token (with inference permissions enabled)
- A Comet Opik account and API key

### Local Setup
1. Clone or download this project workspace.
2. Initialize and activate your Python environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1
   ```
3. Install required software dependencies:
   ```bash
   pip install huggingface_hub python-dotenv opik
   ```
4. Configure your private `.env` file at the project root:
   ```text
   HF_TOKEN=your_hugging_face_token_here
   ```
5. Initialize your Opik dashboard connection:
   ```bash
   opik configure
   ```

### Running the Agent
Execute the main script to chat interactively with your local agent:
```bash
python agent.py
```
