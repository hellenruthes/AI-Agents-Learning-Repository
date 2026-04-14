from agents import Agent
from tools import load_backlog

from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

executor_agent = Agent(
    name="Executor",
    instructions=(
        "You are a Scrum Master. Use the tool load_backlog to analyze the backlog. "
        "Identify risks blockers and priorities."
    ),
    tools=[load_backlog],
)