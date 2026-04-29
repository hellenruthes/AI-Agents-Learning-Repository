# 🧑‍⚖️ Example 2: LLM-as-a-Judge for Tool Usage Evaluation

This example extends Example 1 by adding **LLM-as-a-Judge** to automatically evaluate whether the agent used the correct tools for each query.

---

## 🎯 Objective

Learn how to implement automated quality evaluation for AI agents using:

- **LLM-as-a-Judge pattern**: Using an LLM to evaluate another LLM's behavior
- **Automated scoring**: Quantitative metrics for tool usage correctness
- **Feedback loop**: Scores sent to Langfuse for analysis and improvement

---

## 🆕 What's New in Example 2

### LLM-as-a-Judge Evaluation

After each agent run, a separate LLM call evaluates:

1. **Tool Selection**: Did the agent choose the right tools?
2. **Tool Necessity**: Did it use tools when needed, or avoid them when unnecessary?
3. **Tool Efficiency**: Did it use only the necessary tools, without extras?

### Scoring System

- **Score 1.0**: Perfect tool usage (used exactly the necessary tools)
- **Score 0.5**: Partial correctness (used some correct tools, or used unnecessary ones)
- **Score 0.0**: Incorrect usage (didn't use tools when needed, or used wrong tools)

### Integration with Observability

- Scores are logged to **MLflow** as metrics
- Scores are sent to **Langfuse** with justification comments
- Enables tracking quality trends over time

---

## 🔄 How It Works

```
User Query
    ↓
Agent Execution (with tools)
    ↓
Final Response
    ↓
LLM-as-a-Judge Evaluation
    ↓
Score + Justification
    ↓
Logged to MLflow & Langfuse
```

---

## 🧪 Test Cases

The example includes three test queries designed to evaluate different scenarios:

### 1. Math Query (Should Use Calculator)
**Query**: "What is 1234 multiplied by 56, divided by 7?"

**Expected**: Agent should use `calculator` tool
**Judge Score**: 1.0 if calculator used, 0.0 if not

### 2. Time Query (Should Use Time Tool)
**Query**: "What time is it now?"

**Expected**: Agent should use `get_current_time` tool
**Judge Score**: 1.0 if time tool used, 0.0 if not

### 3. Knowledge Query (Should NOT Use Tools)
**Query**: "What is the capital of France?"

**Expected**: Agent should answer directly without tools
**Judge Score**: 1.0 if no tools used, 0.5 if unnecessary tools used

---

## 📊 Metrics Tracked

### Standard Metrics (from Example 1)
- Input/output tokens
- Total tokens
- Tool calls count
- Iterations
- Latency

### New Metrics
- **judge_score**: Quality score from LLM-as-a-Judge (0.0 to 1.0)

### Langfuse Scores
- **tool_usage_correctness**: Score with justification comment
- Visible in Langfuse dashboard for each trace

---

## 🚀 Running the Example

### Prerequisites

Same as Example 1:
- MLflow running on `http://localhost:5001`
- Environment variables configured (`.env` file)

### Run

```bash
cd examples_exercises/observability/Example2
python agent2.py
```

### Expected Output

```
============================================================
Question 1: What is 1234 multiplied by 56, divided by 7?
============================================================

🔍 Evaluating tool usage...
   Score: 1.0 | Agent correctly used calculator for mathematical operations

Answer:
The result is 9,872.

============================================================
Question 2: What time is it now?
============================================================

🔍 Evaluating tool usage...
   Score: 1.0 | Agent correctly used get_current_time tool

Answer:
It is currently 2026-04-29 14:23:45

============================================================
Question 3: What is the capital of France?
============================================================

🔍 Evaluating tool usage...
   Score: 1.0 | Agent correctly answered without using unnecessary tools

Answer:
The capital of France is Paris.
```

---

## 📈 Viewing Results

### MLflow Dashboard

1. Open `http://localhost:5001`
2. Navigate to "agent-claude" experiment
3. Compare runs by `judge_score` metric
4. Identify patterns in low-scoring runs

### Langfuse Dashboard

1. Login to [Langfuse Cloud](https://cloud.langfuse.com)
2. View traces with scores
3. Filter by `tool_usage_correctness` score
4. Read justification comments for each score

---

## 🎓 Learning Objectives

This example teaches:

1. **LLM-as-a-Judge Pattern**: How to use LLMs to evaluate other LLMs
2. **Automated Quality Metrics**: Quantifying agent behavior
3. **Evaluation Criteria Design**: Defining clear scoring rubrics
4. **Feedback Integration**: Connecting evaluation to observability platforms
5. **Quality Monitoring**: Tracking agent quality over time

---

## 🔧 Customization Ideas

### Extend the Judge

Add more evaluation criteria:
- Response accuracy
- Response completeness
- Tone and style
- Safety and compliance

### Multi-Dimensional Scoring

Evaluate multiple aspects separately:
```python
{
    "tool_selection": 1.0,
    "response_quality": 0.8,
    "efficiency": 0.9,
    "safety": 1.0
}
```

### Threshold Alerts

Set up alerts for low scores:
```python
if score < 0.5:
    send_alert(f"Low quality run: {trace_id}")
```

---

## ⚠️ Important Considerations

### Judge Reliability

- The judge is also an LLM and can make mistakes
- Use multiple judges or human validation for critical applications
- Monitor judge consistency over time

### Cost Implications

- Each agent run triggers an additional LLM call for evaluation
- Consider batching evaluations or sampling for high-volume applications

### Evaluation Bias

- Judge prompts can introduce bias
- Test judge behavior with edge cases
- Iterate on evaluation criteria based on results

---

## 🔥 Common Issues

| Issue | Solution |
|---|---|
| Judge returns invalid JSON | Add error handling and retry logic |
| Scores seem inconsistent | Refine evaluation prompt with more examples |
| High evaluation cost | Sample runs instead of evaluating all |
| Judge too lenient/strict | Adjust scoring criteria in prompt |

---

## 📚 Additional Resources

- [LLM-as-a-Judge Paper](https://arxiv.org/abs/2306.05685)
- [Langfuse Scores Documentation](https://langfuse.com/docs/scores)
- [MLflow Metrics](https://mlflow.org/docs/latest/tracking.html#logging-functions)

---

## 🚀 Next Steps

1. Implement multi-dimensional evaluation
2. Add human feedback collection
3. Create evaluation datasets for regression testing
4. Build dashboards for quality trends
5. Set up automated alerts for quality issues
