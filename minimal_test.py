# minimal_test.py
from google.adk.agents import Agent

agent = Agent(
    model="gemini-2.0-flash-exp",
    name="test_agent",
    instruction="You are a helpful assistant.",
)