Example with ticket 1001
Existing history
client: I cannot log in
agent: You can try resetting your password
client: I already tried and it did not work
Now a new message arrives:
client: Now it says that my account is blocked
If the agent looks only at this new message it may give a generic answer.
But if it has memory it understands that:


the issue started with login


password reset was already attempted


it did not work


now there is new evidence: the account is blocked


So the response can evolve in a more accurate way.

Conceptual flow
new message   ↓save to database (conversations)   ↓retrieve ticket history   ↓recalculate state   ↓save state (ticket_memory)   ↓generate response

python3 insert_message.py