"""
Simple Agent with Anthropic SDK + Langfuse v4 (cloud) + MLflow (local)
+ LLM-as-a-Judge: evaluates if the agent used tools correctly
------------------------------------------------------------------------
Installation:
    pip install anthropic langfuse mlflow python-dotenv
"""

import os
import json
import time
import anthropic
import mlflow
from langfuse import observe, get_client, propagate_attributes
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Clients
# ---------------------------------------------------------------------------
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
langfuse = get_client()

mlflow.set_tracking_uri("http://localhost:5001")

MODEL = "claude-opus-4-5"
MAX_ITERATIONS = 10


# ---------------------------------------------------------------------------
# Available tools for the agent
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "name": "calculator",
        "description": "Performs basic mathematical operations: addition, subtraction, multiplication, and division.",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The operation to be performed.",
                },
                "a": {"type": "number", "description": "First operand."},
                "b": {"type": "number", "description": "Second operand."},
            },
            "required": ["operation", "a", "b"],
        },
    },
    {
        "name": "get_current_time",
        "description": "Returns the current date and time.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "text_analyzer",
        "description": "Analyzes a text and returns statistics: number of words, characters, and sentences.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to be analyzed."}
            },
            "required": ["text"],
        },
    },
]


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------
@observe()
def run_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "calculator":
        a, b = tool_input["a"], tool_input["b"]
        op = tool_input["operation"]
        if op == "add":
            result = a + b
        elif op == "subtract":
            result = a - b
        elif op == "multiply":
            result = a * b
        elif op == "divide":
            result = a / b if b != 0 else "Error: division by zero"
        return str(result)

    elif tool_name == "get_current_time":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    elif tool_name == "text_analyzer":
        text = tool_input["text"]
        words = len(text.split())
        chars = len(text)
        sentences = text.count(".") + text.count("!") + text.count("?")
        return json.dumps({"words": words, "characters": chars, "sentences": sentences})

    return f"Tool '{tool_name}' not found."


# ---------------------------------------------------------------------------
# LLM call
# ---------------------------------------------------------------------------
@observe()
def call_llm(messages: list) -> anthropic.types.Message:
    return client.messages.create(
        model=MODEL,
        max_tokens=4096,
        tools=TOOLS,
        messages=messages,
    )


# ---------------------------------------------------------------------------
# LLM-as-a-Judge: evaluates correct tool usage
# ---------------------------------------------------------------------------
def evaluate_tool_usage(user_message: str, tools_used: list[str], final_response: str) -> dict:
    """
    Uses Claude as a judge to evaluate if the right tools were used.
    Returns score (0.0 to 1.0) and justification.
    """
    tools_available = ["calculator", "get_current_time", "text_analyzer"]

    prompt = f"""You are an expert evaluator of AI agents.

Available tools: {tools_available}
User question: "{user_message}"
Tools used by the agent: {tools_used if tools_used else ["none"]}
Agent's final response: "{final_response[:300]}"

Evaluate if the agent used the CORRECT tools to answer the question.

Criteria:
- Score 1.0: used exactly the necessary tools
- Score 0.5: used partially correct tools or used unnecessary tools
- Score 0.0: didn't use tools when it should have, or used wrong tools

Respond ONLY with JSON in this format (nothing else):
{{"score": 0.0, "justification": "..."}}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )

    result = json.loads(response.content[0].text)
    return result


# ---------------------------------------------------------------------------
# Main agent loop
# ---------------------------------------------------------------------------
@observe()
def run_agent(user_message: str, session_id: str | None = None) -> str:
    mlflow.set_experiment("agent-claude")
    with mlflow.start_run(run_name=f"agent-{int(time.time())}"):
        mlflow.log_param("model", MODEL)
        mlflow.log_param("user_message", user_message[:200])
        mlflow.log_param("session_id", session_id or "no-session")

        with propagate_attributes(session_id=session_id, metadata={"model": MODEL}):
            messages = [{"role": "user", "content": user_message}]
            total_input_tokens = 0
            total_output_tokens = 0
            tools_used = []
            iterations = 0
            start_time = time.time()
            final_text = ""
            trace_id = None

            try:
                while iterations < MAX_ITERATIONS:
                    iterations += 1

                    response = call_llm(messages)

                    # capture trace_id on first iteration
                    if trace_id is None:
                        trace_id = langfuse.get_current_trace_id()

                    total_input_tokens += response.usage.input_tokens
                    total_output_tokens += response.usage.output_tokens

                    if response.stop_reason == "end_turn":
                        final_text = next(
                            (b.text for b in response.content if b.type == "text"), ""
                        )
                        break

                    if response.stop_reason == "tool_use":
                        messages.append({"role": "assistant", "content": response.content})

                        tool_results = []
                        for block in response.content:
                            if block.type != "tool_use":
                                continue

                            tools_used.append(block.name)
                            result = run_tool(block.name, block.input)

                            tool_results.append(
                                {
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": result,
                                }
                            )

                        messages.append({"role": "user", "content": tool_results})

                    else:
                        final_text = "Agent ended without textual response."
                        break

                else:
                    final_text = "Maximum number of iterations reached."

            except Exception as e:
                mlflow.log_param("error", str(e))
                raise

            elapsed = time.time() - start_time

            # ---- LLM-as-a-Judge ----------------------------------------
            print(f"\n🔍 Evaluating tool usage...")
            evaluation = evaluate_tool_usage(user_message, tools_used, final_text)
            score = evaluation["score"]
            justification = evaluation["justification"]

            print(f"   Score: {score} | {justification}")

            # Send score to Langfuse
            if trace_id:
                langfuse.create_score(
                    trace_id=trace_id,
                    name="tool_usage_correctness",
                    value=score,
                    comment=justification,
                )

            # ---- MLflow metrics ----------------------------------------
            mlflow.log_metric("input_tokens", total_input_tokens)
            mlflow.log_metric("output_tokens", total_output_tokens)
            mlflow.log_metric("total_tokens", total_input_tokens + total_output_tokens)
            mlflow.log_metric("tool_calls", len(tools_used))
            mlflow.log_metric("iterations", iterations)
            mlflow.log_metric("latency_seconds", elapsed)
            mlflow.log_metric("judge_score", score)

        langfuse.flush()
        return final_text


# ---------------------------------------------------------------------------
# Usage example
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    questions = [
        "What is 1234 multiplied by 56, divided by 7?",
        "What time is it now?",
        "What is the capital of France?",   # doesn't need tools — judge should penalize if used
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n{'='*60}")
        print(f"Question {i}: {question}")
        print("="*60)

        answer = run_agent(question, session_id=f"demo-session-{i}")
        print(f"\nAnswer:\n{answer}")
