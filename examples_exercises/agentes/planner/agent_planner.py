from agents import Agent

planner_agent = Agent(
    name="Scrum Planner",
    instructions=(
        "You are a planner agent. "
"Receive a backlog and return a short plan in JSON with analysis steps. "
"Consider at least blocked tasks overdue critical items bugs and workload distribution. "
"Respond only with JSON in the format: "
'{"steps": ["...", "...", "..."]}'
    ),
)
