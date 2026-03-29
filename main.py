# main.py
import os
from dotenv import load_dotenv, find_dotenv
from orchestrator.orchestrator import run_pipeline

load_dotenv(find_dotenv(usecwd=True))

if __name__ == "__main__":
    description = """
    A web application with user authentication using modern .NET 8 minimal API,
    React frontend, and Postgres database managed via Entity Framework Core.
    Users can register, log in, and view their profile. 
    JWT-based auth with role support (user, admin).
    """
    
    state = run_pipeline(description)
    
    print("\n=== Pipeline complete ===")
    print(f"Steps completed: {state.completed_steps}")
    
    if state.errors:
        print(f"Errors: {state.errors}")
    else:
        print("Artifacts written to output/")