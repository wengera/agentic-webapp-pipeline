# agents/contract_agent.py
import json
import anthropic
from utils.api import call_with_retry
from orchestrator.state import ProjectState

SYSTEM_PROMPT = """
You are a senior API architect specializing in .NET web applications with Postgres databases.

Your job is to produce the contract that all other agents will build against. 
You must output ONLY valid JSON — no prose, no markdown fences, no explanation.

Given a project description, produce a JSON object with exactly these keys:

{
  "openapi_spec": "<full OpenAPI 3.1 YAML as a string>",
  "shared_models": "<C# record types / DTOs as a string>",
  "auth_contract": {
    "token_type": "Bearer",
    "algorithm": "HS256",
    "claims": ["sub", "email", "role"],
    "scopes": ["read", "write"],
    "expiry_minutes": 60
  }
}

Requirements:
- openapi_spec must include: POST /auth/register, POST /auth/login, GET /auth/me
- All endpoints must declare their request bodies, response schemas, and error responses (400, 401, 500)
- shared_models must use C# record syntax with nullable annotations
- auth_contract must reflect what the JWT middleware in a .NET app needs to validate
- All field names must be snake_case in the API, PascalCase in C# records
"""

def run_contract_agent(state: ProjectState, client: anthropic.Anthropic) -> ProjectState:
    response = call_with_retry(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Project description: {state.project_description}"
            }
        ]
    )
    
    raw = response.content[0].text
    
    # Parse structured output
    result = json.loads(raw)
    
    # Write back to shared state
    state.openapi_spec = result["openapi_spec"]
    state.shared_models = result["shared_models"]
    state.auth_contract = result["auth_contract"]
    
    # Save artifacts to disk
    _save_artifacts(state)
    
    return state

def _save_artifacts(state: ProjectState):
    import os
    os.makedirs("output", exist_ok=True)
    
    with open("output/openapi.yaml", "w") as f:
        f.write(state.openapi_spec)
    
    with open("output/SharedModels.cs", "w") as f:
        f.write(state.shared_models)
    
    with open("output/auth_contract.json", "w") as f:
        import json
        json.dump(state.auth_contract, f, indent=2)