🔎 EXA Tool — What does this tool do?
📌 Overview

The search_external function is an external search tool that allows the agent to access information outside the database using the Exa API.

It simulates an agent that can search the internet.

🧠 Purpose

Enable the agent to:

retrieve up to date information
complement internal data
answer questions not available in the database
⚙️ How it works
1. Authentication

The tool uses an API key:

EXA_API_KEY = os.getenv("EXA_API_KEY")

This key allows access to the Exa service.

2. Client creation
exa = Exa(EXA_API_KEY)

This creates the client responsible for communicating with the API.

3. Content search
response = exa.search_and_contents(
    query,
    num_results=5,
    use_autoprompt=True,
    text=True
)

This call:

receives a query
searches for relevant web content
returns results with text and metadata
4. Result structure

Each result is converted into a dictionary:

{
    "source": "external",
    "title": item.title,
    "text": item.text,
    "url": item.url
}
📦 Function output

The function returns a list:

[
    {
        "source": "external",
        "title": "Login troubleshooting guide",
        "text": "...",
        "url": "https://..."
    }
]