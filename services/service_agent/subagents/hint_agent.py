from google.adk.agents import LlmAgent
from google.genai import types
hint_agent = LlmAgent(
    name="hint_agent",

    model="gemini-2.5-flash-lite",

    description="""Gives progressive hints for problems""",

    instruction="""
    Give only hints.

    Do not reveal full solution.

    Hint Levels:
    Level1 -> Direction
    Level2 -> Approach
    Level3 -> Near Solution

    Keep answer concise.
    """,
       generate_content_config=types.GenerateContentConfig(
        max_output_tokens=200,
        temperature=0.2
    )
)