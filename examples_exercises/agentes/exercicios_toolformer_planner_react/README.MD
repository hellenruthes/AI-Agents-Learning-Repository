EXERCISE 1 — Basic Toolformer (Ticket)
Objective

Create an agent that decides when to use a tool to retrieve a ticket.

Context

You already have:

conversations table
get_ticket_conversation tool
Prompt

Create an agent that receives questions about tickets.

If the question includes a ticket_id the agent must use the tool.

Example inputs
"Is ticket 1001 resolved?"
"What is a ticket?"
✅ Expected behavior
Uses the tool for the first input
Does NOT use the tool for the second input
EXERCISE 2 — ReAct (Ticket Analysis)
Objective

Make the agent retrieve data and reason about it.

Context

Same get_ticket_conversation tool.

Prompt

Create an agent that:

receives a ticket_id
uses the tool to retrieve the conversation
responds with:
current status
last client message
suggested next step
Example

"Analyze ticket 1007"

✅ Expected behavior

Structured response such as:

Status: open
Last message: ...
Next step: ...
EXERCISE 3 — Planner + Executor (Scrum Backlog)
Objective

Separate planning from execution.

Context
backlog table
load_backlog tool
Prompt

Create two agents:

1. Planner

Receives:

"Analyze the sprint backlog"

It must generate a JSON plan with steps such as:

check blocked tasks
identify delays
analyze bugs
evaluate workload distribution
2. Executor

Receives:

the plan
access to the backlog through the tool

It must:

execute the analysis
identify risks
suggest improvements
✅ Expected behavior
Planner
{
  "steps": ["...", "..."]
}
Executor
- Blocked tasks: ...
- Risks: ...
- Suggestions: ...