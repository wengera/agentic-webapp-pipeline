# orchestrator/orchestrator.py
import anthropic
import json
from orchestrator.state import ProjectState
from agents.contract_agent import run_contract_agent

client = anthropic.Anthropic()

# This is the sequence the orchestrator follows.
# Add new agents here as you build them.
PIPELINE_STEPS = [
    "contract",
    # "frontend",   # wire in later
    # "backend",    # wire in later
    # "database",   # wire in later
    # "tests",      # wire in later
    # "security",   # wire in later
    # "review",     # wire in later
]

def run_pipeline(project_description: str) -> ProjectState:
    state = ProjectState(project_description=project_description)
    
    print(f"\n=== Pipeline starting ===")
    print(f"Project: {project_description}\n")
    
    for step in PIPELINE_STEPS:
        if state.is_done(step):
            print(f"[{step}] already complete, skipping")
            continue
        
        print(f"[{step}] running...")
        
        try:
            if step == "contract":
                state = run_contract_agent(state, client)
            # elif step == "frontend":
            #     state = run_frontend_agent(state, client)
            # ... add agents as you build them
            
            state.mark_done(step)
            print(f"[{step}] done\n")
            
        except Exception as e:
            error_msg = f"[{step}] failed: {str(e)}"
            state.errors.append(error_msg)
            print(f"ERROR: {error_msg}")
            break  # stop pipeline on failure — don't cascade bad state
    
    return state


def call_with_retry(client, **kwargs):
    while True:
        try:
            return client.messages.create(**kwargs)
        except anthropic.RateLimitError:
            print("Rate limited, waiting 15s...")
            time.sleep(15)