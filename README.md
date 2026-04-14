
⚙️ Setup
Prerequisites
Docker and Docker Compose installed
API keys configured in the .env file (Anthropic, OpenAI, Gemini)
🐳 Docker Setup (Recommended)

The full environment runs in containers, including both the database and the Python application. No local virtual environment, pip install, or specific Python version is required on your machine.

1. Start all services
docker compose up -d

This starts:

agentes_postgres — PostgreSQL 16 with the suporte_ai database
agentes_app — Python 3.12 with all required dependencies installed

The app service only starts after PostgreSQL is ready, using a health check.

2. Load data into the database
docker compose exec app python load_data.py
3. Run scripts
docker compose exec app python exemplos_exercicios/agentes/exe1/run_support_agent.py
4. Open an interactive shell
docker compose exec app bash

Inside the container, you can run any script normally.

5. Stop all services
docker compose down

To remove the database data as well:

docker compose down -v
🐍 Local Setup (Alternative Without Docker)

If you prefer to run the project locally, you need Python 3.9+ and a PostgreSQL instance running on port 5432.

1. Create a virtual environment
python -m venv .venv

Mac/Linux

source .venv/bin/activate

Windows

.venv\Scripts\activate
2. Install dependencies
pip install -r requirements.txt
3. Start only the database with Docker
docker compose up -d postgres
4. Load the data
python load_data.py
5. Run scripts
python exemplos_exercicios/agentes/exe1/run_support_agent.py
🔐 Environment Variables

The exemplos_exercicios/.env file must include:

SUMMARY_MAX_POINTS=4
SUMMARY_SENTIMENT=true
SUMMARY_PRIORITY_RULES=true
ANTHROPIC_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here
GEMINI_API_KEY=your-key-here

In the Docker setup, the env_file setting in docker-compose.yml automatically loads these variables into the container.

📊 Checking the Database
Using Docker
docker exec -it agentes_postgres psql -U admin -d suporte_ai

Inside psql, run:

\dt
SELECT COUNT(*) FROM conversations;
SELECT COUNT(*) FROM feedbacks;

Expected tables:

conversations
agent_configs
agent_runs
feedbacks
🔥 Common Issues
Problem	Solution
Docker does not connect	Open Docker Desktop and make sure it is running
Port 5432 is already in use	Change it in docker-compose.yml to "5433:5432"
Table does not exist	Run docker compose down -v and start again
Error pulling image	Run docker pull postgres:16 or disable VPN
Agents

Path: /agentes_B2_S01-02/exemplos_exercicios/agentes/

exe1 — Getting Started
🎯 Learning Objective

This exercise is designed to demonstrate:

how to structure a basic agent workflow
how to organize input → processing → output
the limitations of purely deterministic approaches

It serves as a foundation for comparison with more advanced versions, especially LLM-based agents that can better handle natural language and ambiguity.

The first exercise consists of building a simple support agent based on fixed rules, without using language models.

How It Works

This agent receives a ticket ID, retrieves the associated conversation, and performs three main tasks:

a) Classifies the problem category
b) Checks whether follow-up is needed
c) Generates a summary of the conversation

The logic is deterministic and based on keywords. For example, terms such as “login,” “password,” or “access” classify the ticket as a login issue, while terms such as “payment” or “card” indicate billing or financial issues.

⚙️ Main Characteristics
Does not use AI or LLMs
Works with explicit rules (if/else)
Fully predictable and controllable
Low computational cost
Easy to understand and debug
⚠️ Limitations

Although functional, this agent has important limitations:

Depends on exact words and does not understand language variation
Does not capture context or intent
Is difficult to scale because rules grow quickly
Can fail easily in ambiguous cases
How to Run

Go to the folder and run:

python3 run_support_agent.py <ticket_id>

or

python run_support_agent.py <ticket_id>
🧠 Exercise 2 — Support Agent with LLM and Tool Calling
🎯 Learning Objective

This exercise demonstrates:

how to build agents with LLMs
how to integrate external tools
how to work with structured outputs
the importance of control and validation in AI systems

In the second exercise, the support agent evolves to use a language model with the ability to make decisions and dynamically call tools.

Instead of following fixed rules, the agent interprets the conversation context and decides which actions to perform, such as:

a) Retrieving the ticket conversation
b) Classifying the category
c) Identifying whether follow-up is required
d) Generating a summary

This is done through tool calling, where the model chooses which functions to use during execution.

⚙️ Main Characteristics
Uses an LLM (for example, Gemini)
Supports dynamic decision-making
Integrates with external tools and functions
Produces structured output (JSON)
Is more flexible and adaptable
🔄 How It Works

The agent flow becomes:

User → LLM → decides which tool to call → executes tool → returns result → LLM continues → final response

In other words, the LLM acts as an intelligent orchestrator, not just a text generator.

Improvements Over Exercise 1
Understands variations in natural language
Does not depend on exact keywords
Is more robust in real-world scenarios
Reduces the need for manual rules
Scales more easily to new use cases
Data Visualization Tool

In addition to the LLM and tools, the exercise includes a local PostgreSQL database. In this context, DBeaver is useful for exploring tickets, validating queries, and giving students a more concrete view of how the agent interacts with real data.

💻 How to Download and Use DBeaver
🧭 What Is DBeaver?

DBeaver is a tool used to:

connect to databases
view tables
run SQL queries
explore data
⬇️ 1. Download

Go to:
DBeaver download page

Choose:

DBeaver Community (free)

Download the version for your system:

Mac (.dmg)
Windows (.exe)
Linux
⚙️ 2. Installation

Mac

Open the .dmg
Drag the app to Applications

Windows

Next → Next → Install

The default installation is fine.

🚀 3. Open DBeaver and Create a Connection
Open DBeaver
Click New Database Connection
Select PostgreSQL
🔌 4. Connect to the Database (Docker)

Using your docker-compose setup, enter:

Host: localhost
Port: 5432
Database: suporte_ai
Username: admin
Password: admin123

Then click:

Test Connection
Finish
🧪 5. View the Data

After connecting:

Expand: database → schemas → public → tables

You should see your tables, such as tickets.

Then:

Right-click → View Data
💡 6. Run SQL Queries

Right-click and open SQL Editor

Then run:

SELECT * FROM conversations;

or

SELECT * FROM agent_runs;
Additional Tools
Qdrant
http://localhost:6333/dashboard#/console
Langfuse

Run:

chmod +x start_langfuse.sh
./start_langfuse.sh
If docker compose down and docker compose up -d Do Not Solve the Problem

Run:

docker rm -f agentes_pgadmin agentes_postgres agentes_qdrant