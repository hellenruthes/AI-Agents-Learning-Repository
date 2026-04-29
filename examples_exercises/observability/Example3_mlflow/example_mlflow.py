"""
Experiment: compare agent temperatures
---------------------------------------
Easy to adapt to compare models, prompts, max_tokens, etc.

Installation:
    pip install anthropic langfuse mlflow python-dotenv
"""

import os
import json
import time
from datetime import datetime
import anthropic
import mlflow
from langfuse import observe, get_client, propagate_attributes
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
langfuse = get_client()

mlflow.set_tracking_uri("http://localhost:5001")

# ---------------------------------------------------------------------------
# ✏️ CONFIGURE YOUR EXPERIMENT HERE
# Change the values below to compare other variables
# ---------------------------------------------------------------------------
EXPERIMENT_NAME = "temperature-comparison"

VARIATIONS = [
    {"temperature": 0.0},
    {"temperature": 0.5},
    {"temperature": 1.0},
]

# Questions used in ALL variations (for fair comparison)
QUESTIONS = [
    "Create a creative metaphor to explain what artificial intelligence is.",
    "Summarize in one sentence: 'The sky is blue because air molecules scatter blue light more than other colors.'",
]

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "name": "word_counter",
        "description": "Counts words, characters, and sentences in a text.",
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string"}
            },
            "required": ["text"],
        },
    },
]

def run_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "word_counter":
        text = tool_input["text"]
        words = len(text.split())
        chars = len(text)
        sentences = sum(text.count(p) for p in [".", "!", "?"])
        return json.dumps({"words": words, "characters": chars, "sentences": max(sentences, 1)})
    return f"Tool '{tool_name}' not found."


# ---------------------------------------------------------------------------
# Parameterized agent
# Receives config as argument — easy to vary
# ---------------------------------------------------------------------------
def run_agent(user_message: str, config: dict, session_id: str | None = None) -> dict:
    """
    Runs the agent with the provided config.
    Returns a dict with the response and collected metrics.
    """
    model = config.get("model", "claude-haiku-4-5")
    temperature = config.get("temperature", 1.0)
    max_tokens = config.get("max_tokens", 1024)

    messages = [{"role": "user", "content": user_message}]
    total_input_tokens = 0
    total_output_tokens = 0
    tools_used = []
    iterations = 0
    start_time = time.time()
    final_text = ""

    with propagate_attributes(session_id=session_id, metadata={"model": model, "temperature": temperature}):
        while iterations < 10:
            iterations += 1

            response = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                tools=TOOLS,
                messages=messages,
            )

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
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
                messages.append({"role": "user", "content": tool_results})

    elapsed = time.time() - start_time

    return {
        "response": final_text,
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
        "total_tokens": total_input_tokens + total_output_tokens,
        "tool_calls": len(tools_used),
        "iterations": iterations,
        "latency_seconds": round(elapsed, 2),
    }


# ---------------------------------------------------------------------------
# Experiment runner
# ---------------------------------------------------------------------------
def run_experiment():
    mlflow.set_experiment(EXPERIMENT_NAME)

    print(f"\n🧪 Experiment: {EXPERIMENT_NAME}")
    print(f"   {len(VARIATIONS)} variations x {len(QUESTIONS)} questions\n")

    for variation in VARIATIONS:
        # Run name describes the variation
        run_name = "_".join(f"{k}={v}" for k, v in variation.items())

        print(f"\n{'='*60}")
        print(f"🔧 Variation: {variation}")
        print(f"{'='*60}")

        # Complete config = defaults + current variation
        config = {
            "model": "claude-haiku-4-5",
            "temperature": 1.0,
            "max_tokens": 1024,
            **variation,  # overrides with current variation
        }

        with mlflow.start_run(run_name=run_name):
            # Log complete config as params
            for k, v in config.items():
                mlflow.log_param(k, v)

            # Accumulate metrics from all questions
            total_metrics = {
                "total_tokens": 0,
                "latency_seconds": 0,
                "tool_calls": 0,
            }

            for i, question in enumerate(QUESTIONS, 1):
                print(f"\n  Question {i}: {question[:60]}...")

                result = run_agent(
                    question,
                    config=config,
                    session_id=f"{run_name}-q{i}",
                )

                print(f"  Response: {result['response'][:100]}...")
                print(f"  Tokens: {result['total_tokens']} | Latency: {result['latency_seconds']}s")

                total_metrics["total_tokens"] += result["total_tokens"]
                total_metrics["latency_seconds"] += result["latency_seconds"]
                total_metrics["tool_calls"] += result["tool_calls"]

                # Log metrics per question (with step = question index)
                mlflow.log_metric("tokens_per_question", result["total_tokens"], step=i)
                mlflow.log_metric("latency_per_question", result["latency_seconds"], step=i)

            # Log variation averages
            n = len(QUESTIONS)
            mlflow.log_metric("average_tokens", total_metrics["total_tokens"] / n)
            mlflow.log_metric("average_latency", total_metrics["latency_seconds"] / n)
            mlflow.log_metric("total_tool_calls", total_metrics["tool_calls"])

    langfuse.flush()
    print(f"\n✅ Experiment completed! View results at http://localhost:5001")


if __name__ == "__main__":
    run_experiment()
