# dev_pipeline

An agentic development pipeline that builds a full-stack web application from a plain-English description. Each stage of the build is handled by a specialized AI agent — orchestrated in sequence, sharing state through a single pipeline object.

The target output is a modern **.NET 8 minimal API** backend, **React** frontend, and **Postgres** database managed via **Entity Framework Core**, with JWT-based authentication.

---

## How it works

A central orchestrator reads a project description and runs a sequence of specialist agents one by one. Each agent calls Claude with a focused system prompt, produces structured output, and writes its results back to a shared `ProjectState` object. Downstream agents can read the outputs of upstream agents — so the backend agent knows exactly what the contract agent defined, and the test agent knows exactly what the backend agent produced.

```
main.py
  └── orchestrator
        ├── contract agent   → openapi.yaml, SharedModels.cs, auth_contract.json
        ├── frontend agent   → React components, auth UI, API client
        ├── backend agent    → .NET 8 minimal API, JWT middleware, controllers
        ├── database agent   → EF Core entities, migrations, DbContext
        ├── test agent       → unit + integration tests, auth flow coverage
        ├── security agent   → OWASP review, secrets check, hardening report
        └── review agent     → lint, conventions, final diff summary
```

The pipeline halts on the first failure — bad output from one agent won't cascade into downstream agents.

---

## Project structure

```
dev_pipeline/
├── main.py                   # Entry point — edit the project description here
├── requirements.txt
├── .env                      # ANTHROPIC_API_KEY goes here
│
├── orchestrator/
│   ├── __init__.py
│   ├── orchestrator.py       # Pipeline sequencer
│   └── state.py              # Shared ProjectState dataclass
│
├── agents/
│   ├── __init__.py
│   ├── contract_agent.py     # OpenAPI spec, DTOs, auth contract
│   ├── frontend_agent.py     # (coming soon)
│   ├── backend_agent.py      # (coming soon)
│   ├── database_agent.py     # (coming soon)
│   ├── test_agent.py         # (coming soon)
│   ├── security_agent.py     # (coming soon)
│   └── review_agent.py       # (coming soon)
│
├── prompts/                  # Optional: store system prompts as .md files
│
└── output/                   # Generated artifacts land here
    ├── openapi.yaml
    ├── SharedModels.cs
    └── auth_contract.json
```

---

## Setup

**1. Clone and create a virtual environment**

```bash
git clone <your-repo>
cd dev_pipeline
python -m venv .venv
source .venv/bin/activate        # Windows WSL: source .venv/bin/activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Add your Anthropic API key**

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-...
```

Get your key from [console.anthropic.com](https://console.anthropic.com) → Settings → API Keys. Note that API access requires credits — there is no free tier (separate from claude.ai).

If you hit `.env` loading issues in WSL, export the key directly in your shell session instead:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

**4. Run the pipeline**

```bash
python main.py
```

Generated files will appear in `output/`.

---

## Configuring the project description

Edit the `description` string in `main.py` to describe what you want to build:

```python
description = """
A web application with user authentication using modern .NET 8 minimal API,
React frontend, and Postgres database managed via Entity Framework Core.
Users can register, log in, and view their profile.
JWT-based auth with role support (user, admin).
"""
```

The more specific you are, the better the contract agent's output will be. Include domain details, role types, any specific endpoints you know you need.

---

## Adding a new agent

1. Create `agents/your_agent.py` with a `run_your_agent(state, client)` function
2. Read what you need from `state` (e.g. `state.openapi_spec`)
3. Write your output back to `state` (e.g. `state.frontend_code = ...`)
4. Add `"your_step"` to `PIPELINE_STEPS` in `orchestrator/orchestrator.py`
5. Add the corresponding `elif` branch in `run_pipeline()`

---

## Requirements

- Python 3.11+
- Anthropic API key with available credits
- WSL or Linux/macOS recommended (Windows native untested)

```
anthropic>=0.25.0
python-dotenv>=1.0.0
pyyaml>=6.0
```

---

## Current status

| Agent | Status |
|---|---|
| Orchestrator | Working |
| Contract + spec | Working |
| Frontend | Planned |
| Backend | Planned |
| Database | Planned |
| Test generation | Planned |
| Security review | Planned |
| Code review | Planned |

---

## Notes for WSL users

- Keep your project files under `/mnt/c/...` or move them to the Linux filesystem (`~/`) for better performance
- If `python-dotenv` can't find your `.env`, use `find_dotenv(usecwd=True)` or export the key manually
- Use `python3` instead of `python` if the default Python points to 2.x