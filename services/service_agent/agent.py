import os
from google.adk.agents import LlmAgent
from .subagents.problem_solver import problem_solver
from .subagents.hint_agent import hint_agent
from .subagents.complexity_agent import complexity_agent
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# env_path = Path(__file__).parent/".env"
# print(env_path)
# load_dotenv(env_path)
# print("PWD=",os.getcwd())
# print("KEY=",os.getenv("GOOGLE_API_KEY"))



root_agent = LlmAgent(
    name="leetcode_tutor",
    model="gemini-2.5-flash-lite",

    description="""
    You are Concis Leetcode Tutor
    Main tutoring orchestrator.
    Routes request to specific agents.
    """,

    instruction="""
    Determine user intent.

    if user ask for:
    - Full explanation -> problem_solver
    - Hint -> hint_agent
    - Complexity -> complexity_agent

    Route accordingly

     -Use Markdown Formatting
            Use:
            -headings
            -bullent point
            -numbered list
            -code blokcs
            -bold text
    """,

    sub_agents=[
        problem_solver,
        hint_agent,
        complexity_agent
    ]
)