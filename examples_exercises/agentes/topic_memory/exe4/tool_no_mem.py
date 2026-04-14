def analyze_without_history(message: str) -> dict:
    prompt = f"""
You are a customer support analyst.

Analyze only the message below WITHOUT considering any previous history.

Your task is:
1. Identify the issue category
2. Summarize the problem
3. Suggest the first action
4. Explicitly state that there is no history

Possible categories:
- access
- payment
- delivery
- cancellation
- account
- others

Respond in JSON with:
- category
- summary
- first_action
- note

Message:
{message}
"""