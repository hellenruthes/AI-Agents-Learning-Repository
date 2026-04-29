Exercise: Enriching Internal Data with External Search
Objective

Create a flow in which the system:

analyzes internal data from the database
identifies the most recurring topics
uses an external tool to search for complementary content
organizes the results to support analysis or customer support
Scenario

You have two tables in the database:

conversations
feedbacks

These tables contain user complaints questions and feedback.

Your task will be to:

identify the most frequent topics
search for external articles about those topics using Exa
save those files as .txt in the exe8/arquivos folder
What students should build
Part 1 — Identify frequent topics

Create a function that analyzes conversations or feedbacks and finds the most recurring topics.

Example topics:

login
payment
slowness
freezing
delivery
cancellation

They can do this using keywords.

Example:

def get_top_topics(feedbacks_df) -> list[tuple[str, int]]:
    ...

Expected output:

[
    ("payment", 8),
    ("login", 6),
    ("slowness", 5)
]
Part 2 — Create the external tool

Create a tool using Exa to search for articles related to each topic.

Example:

def search_external_articles(topic: str) -> list[dict]:
    ...

Expected output:

[
    {
        "topic": "payment",
        "title": "Common Causes of Payment Failures",
        "url": "...",
        "text": "..."
    }
]
Part 3 — Enrich the topics

For each frequent topic search for 2 or 3 external articles.

Example:

def enrich_topics_with_external_articles(topics: list[str]) -> dict:
    ...

Expected output:

{
    "payment": [...],
    "login": [...],
    "slowness": [...]
}
Part 4 — Display the result

Show something like:

Most frequent topics:
1. payment (8)
2. login (6)
3. slowness (5)

External articles found:

[payment]
- ...
- ...

[login]
- ...
- ...

[slowness]
- ...
- ...