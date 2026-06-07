from google.adk.agents import LlmAgent
from google.genai import types
complexity_agent = LlmAgent(
    name="complexity_agent",

    model="gemini-2.5-flash-lite",

    description="""Analyzes algorithm complexity""",

    instruction="""
    Analyze:

    - Time complexity
    - Space complexity
    - Bottlenecks
    - Possible optimization

    Keep response technical
    """,
        generate_content_config=types.GenerateContentConfig(
        max_output_tokens=400,
        temperature=0.2
    )
)