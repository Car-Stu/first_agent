# Local AI Assistant with LLMops Infrastructure — Project Summary

## Overview
A stateful, conversational AI agent built from scratch, taken from a bare Python
script to a fully deployed, observable, tested, and continuously integrated
web application. The project mirrors the architecture of production-grade
LLMops repositories: modular code, live tracing, automated tests, CI on every
push, and CD to a public web app.

## Architecture

```
first_agent/
├── main.py                      # Streamlit UI — owns all chat state
├── src/
│   └── agent/
│       └── core.py              # Backend logic — model calls, no side effects on state
├── test_agent.py                # pytest suite
├── requirements.txt             # dependency manifest for CI/CD
├── .env                         # local secrets (gitignored)
├── .gitignore
└── .github/
    └── workflows/
        └── test.yml             # GitHub Actions CI pipeline
```

**Design principle established during the build:** the UI layer (`main.py`)
is the single source of truth for `chat_history` state. The backend
(`core.py`) is a pure function — it reads history, calls the model, and
returns a reply without mutating anything it was passed. Violating this
(letting both layers append to the same list) was the root cause of the
hardest bug in the project (duplicate/delayed responses).

## Tools & Services Used

| Tool | Role |
|---|---|
| **Python 3.11** | Core language |
| **Streamlit** | Web UI / chat interface, deployed via Streamlit Community Cloud |
| **Hugging Face Inference Providers** (`router.huggingface.co/v1`) | LLM serving, accessed via the OpenAI-compatible API |
| **OpenAI Python SDK** (`openai` package) | Client used to call the HF router in a standardized way |
| **DeepSeek-V3-0324** (`deepseek-ai/DeepSeek-V3-0324`) | The LLM ultimately used — ungated, supported by the router |
| **Opik (Comet)** | LLMops observability — traces every call, latency, token usage, via `@track` decorator |
| **pytest** | Automated unit testing (`test_agent.py`) |
| **GitHub Actions** | CI — runs the test suite on every push/PR |
| **GitHub Secrets** | Secure storage of `HF_TOKEN` / `OPIK_API_KEY` for CI |
| **python-dotenv** | Local secret management via `.env` |
| **Git / GitHub** | Version control, remote repo, branch protection groundwork |
| **VS Code + PowerShell** | Local dev environment |

## Build Phases

1. **Local foundation** — virtual environment, `.env` secret vault, first working
   script calling an LLM.
2. **Observability** — Opik tracing wired in via a `@track` decorator on the
   core generation function.
3. **Modular architecture** — split a single script into `src/agent/core.py`
   (backend) and `main.py` (interface), following the separation-of-concerns
   pattern used in production repos.
4. **Testing** — `pytest` suite validating the core function returns a
   non-empty string response.
5. **CI** — GitHub Actions workflow (`.github/workflows/test.yml`) running
   pytest on every push, authenticated via GitHub Secrets.
6. **CD** — deployed to Streamlit Community Cloud, linked directly to the
   GitHub repo for automatic redeploys on push.
7. **Conversational memory** — moved from single-turn to multi-turn chat using
   `st.session_state` and a running message history array.

## Key Bugs Fixed (and the lessons behind them)

- **Wrong API endpoint**: `base_url` was pointed at the public website
  (`https://huggingface.co`) instead of the actual API gateway
  (`https://router.huggingface.co/v1`) — caused HTML/login pages to be
  returned instead of JSON.
- **Gated models**: `Mistral-7B-Instruct-v0.3` and `Llama-3.1-8B-Instruct`
  require accepting a license on the HF website before a token can call
  them — caused inconsistent behavior between local runs and CI.
  Resolved by using ungated models.
- **Model availability drift**: `Qwen2.5-7B-Instruct` stopped being served by
  any provider on the router (`model_not_supported`) — resolved by switching
  to a currently-supported model (`DeepSeek-V3-0324`).
- **Response parsing**: `response.choices.message.content` is invalid;
  the correct access pattern is `response.choices[0].message.content`.
- **Shared mutable state bug (the big one)**: `core.py` appended the
  assistant's reply directly onto the same list object passed in from
  `st.session_state.chat_history`, while `main.py` *also* appended it —
  causing every response to render twice and appear one turn late.
  Fixed by making `core.py` never mutate its input; state ownership moved
  entirely to the UI layer.
- **CI/CD environment parity**: local `.env` values are invisible to GitHub
  Actions and Streamlit Cloud — both needed the same keys added to their
  respective secret managers before the pipeline could pass end-to-end.

## Final State
- ✅ Multi-turn conversational memory works correctly in the browser
- ✅ Live Opik dashboard traces every call (prompt, latency, tokens)
- ✅ `pytest` suite passes locally and in CI
- ✅ GitHub Actions shows a green checkmark on every push
- ✅ App is live and auto-redeploys via Streamlit Cloud CD

## Possible Next Steps
- Add tool-calling / function-calling (e.g. a live search or database lookup)
- Add a "reset conversation" button
- Isolate Opik traces into a dedicated project instead of the shared default
- Reuse this modular core+tracing+CI/CD pattern for the NOC Copilot dissertation project
