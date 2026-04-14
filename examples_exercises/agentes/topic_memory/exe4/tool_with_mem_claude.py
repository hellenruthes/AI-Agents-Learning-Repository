from sqlalchemy import create_engine, text
import json
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

# Initialize Claude client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

DB_URL = "postgresql+psycopg2://admin:admin123@localhost:5433/suporte_ai"
engine = create_engine(DB_URL)

# =========================================================
# TOOL 1: GET CONVERSATION (MEMORY)
# =========================================================

def get_ticket_conversation(ticket_id: int) -> dict:
    query = text("""
        SELECT speaker, message, timestamp, ticket_status
        FROM conversations
        WHERE ticket_id = :ticket_id
        ORDER BY timestamp
    """)

    with engine.begin() as conn:
        rows = conn.execute(query, {"ticket_id": ticket_id}).mappings().all()

    if not rows:
        return {
            "ticket_id": ticket_id,
            "found": False,
            "conversation_text": ""
        }

    conversation_text = "\n".join(
        f"{row['speaker']}: {row['message']}"
        for row in rows
    )

    return {
        "ticket_id": ticket_id,
        "found": True,
        "conversation_text": conversation_text
    }


# =========================================================
# TOOL 2: CLASSIFICATION
# =========================================================

def classify_category_prompt(conversation_text: str) -> dict:
    prompt = f"""
You are a support ticket classifier.

Classify the conversation into only one of the categories below:
- access
- payment
- delivery
- cancellation
- account
- others

Respond ONLY with valid JSON with the key "category".

Conversation:
{conversation_text}
"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        result = json.loads(response.content[0].text)

        return {
            "category": result["category"],
            "method": "llm_claude"
        }

    except Exception as e:
        print("Error classify_category_prompt:", e)
        return {
            "category": "others",
            "method": "fallback_error"
        }


# =========================================================
# TOOL 3: ANALYZE WITH MEMORY
# =========================================================

def analyze_with_memory(ticket_id: int, new_message: str) -> dict:
    conversation = get_ticket_conversation(ticket_id)

    if not conversation["found"]:
        return {
            "ticket_id": ticket_id,
            "category": "others",
            "summary": "No history found for this ticket.",
            "recommended_action": "Analyze the new message independently or verify if the ticket exists.",
            "note": "Analysis with memory requested but no history available.",
            "method": "no_history_available"
        }

    conversation_text = conversation["conversation_text"]

    prompt = f"""
You are a customer support analyst.

Analyze the NEW message considering the ticket HISTORY.

Your task is:
1. Identify the main category of the case
2. Summarize the current issue considering the history
3. Explain what has already been attempted or communicated
4. Suggest the next recommended action
5. Explicitly state that the analysis used historical context

Possible categories:
- access
- payment
- delivery
- cancellation
- account
- others

Respond ONLY with valid JSON containing:
- category
- summary
- relevant_context
- recommended_action
- note

Ticket history:
{conversation_text}

New message:
{new_message}
"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text.strip()

        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[1] if "\n" in response_text else response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()

        result = json.loads(response_text)

        return {
            "ticket_id": ticket_id,
            "category": result["category"],
            "summary": result["summary"],
            "relevant_context": result["relevant_context"],
            "recommended_action": result["recommended_action"],
            "note": result["note"],
            "method": "llm_claude_with_memory"
        }

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Full response: {response_text if 'response_text' in locals() else 'N/A'}")

        return {
            "ticket_id": ticket_id,
            "category": "others",
            "summary": "Could not analyze the message with history.",
            "relevant_context": "History retrieved but JSON parsing failed.",
            "recommended_action": "Retry analysis or review prompt or model.",
            "note": "Analysis with history fallback due to JSON error.",
            "method": "fallback_json_error"
        }

    except Exception as e:
        print("Error analyze_with_memory:", e)

        return {
            "ticket_id": ticket_id,
            "category": "others",
            "summary": "Could not analyze the message with history.",
            "relevant_context": "History retrieved but analysis failed.",
            "recommended_action": "Retry analysis or review prompt or model.",
            "note": "Analysis with history fallback due to error.",
            "method": "fallback_error"
        }


# =========================================================
# TOOL 4: FOLLOW-UP
# =========================================================

def detect_followup(conversation_text: str) -> dict:
    lines = [line.strip() for line in conversation_text.split("\n") if line.strip()]

    if not lines:
        return {
            "needs_followup": False,
            "reason": "no messages",
            "last_message_from_agent": False
        }

    last_line = lines[-1].lower()
    last_message_from_agent = last_line.startswith("agent:")

    return {
        "needs_followup": last_message_from_agent,
        "reason": (
            "last message was from agent"
            if last_message_from_agent
            else "last message was from client"
        ),
        "last_message_from_agent": last_message_from_agent
    }


# =========================================================
# TOOL 5: LOG EXECUTION
# =========================================================

def save_agent_run(agent_name: str, ticket_id: int, input_text: str, output_text: dict) -> None:
    query = text("""
        INSERT INTO agent_runs (
            agent_name,
            ticket_id,
            input_text,
            output_text
        )
        VALUES (
            :agent_name,
            :ticket_id,
            :input_text,
            :output_text
        )
    """)

    with engine.begin() as conn:
        conn.execute(
            query,
            {
                "agent_name": agent_name,
                "ticket_id": ticket_id,
                "input_text": input_text,
                "output_text": json.dumps(output_text, ensure_ascii=False)
            }
        )


# =========================================================
# TOOL MAP
# =========================================================

TOOL_MAP = {
    "get_ticket_conversation": get_ticket_conversation,
    "classify_category_prompt": classify_category_prompt,
    "detect_followup": detect_followup,
    "analyze_with_memory": analyze_with_memory,
}


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    ticket_id = 1001
    new_message = "Now it says that my account is blocked"

    print("\n==============================")
    print("ANALYSIS WITH MEMORY (CLAUDE)")
    print("==============================\n")

    result = analyze_with_memory(ticket_id, new_message)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    # Optional: log execution
    save_agent_run(
        agent_name="analyze_with_memory_claude",
        ticket_id=ticket_id,
        input_text=new_message,
        output_text=result
    )