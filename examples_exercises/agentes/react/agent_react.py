from agents import Agent
from tools import get_ticket_conversation

react_agent = Agent(
    name="Support ReAct Agent",
    instructions=(
        "You are a support agent.\n"
        "Always use the tool get_ticket_conversation.\n"
        "Return status last message and next step."
    ),
    tools=[get_ticket_conversation],
)