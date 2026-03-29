# orchestrator/state.py
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ProjectState:
    # What we're building
    project_description: str = ""
    
    # Outputs from each agent — populated as the pipeline runs
    openapi_spec: Optional[str] = None        # YAML string
    shared_models: Optional[str] = None       # C# DTO classes
    auth_contract: Optional[dict] = None      # JWT shape, claims, scopes
    
    frontend_code: Optional[str] = None
    backend_code: Optional[str] = None
    db_migrations: Optional[str] = None
    test_suite: Optional[str] = None
    security_report: Optional[str] = None
    
    # Pipeline control
    completed_steps: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    
    def mark_done(self, step: str):
        self.completed_steps.append(step)
    
    def is_done(self, step: str) -> bool:
        return step in self.completed_steps