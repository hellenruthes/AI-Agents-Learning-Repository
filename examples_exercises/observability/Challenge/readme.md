# 🧪 Advanced Exercises: Production Agent Monitoring

## Exercise 3 — Regression Detection

### 📖 Context

Imagine you work on the AI team of an e-commerce company. You have a customer service agent running in production for 3 months. The product team asked you to improve the tone of responses — the agent was being too dry with customers.

You update the system prompt and do a quick test: looks better! You deploy it.

Two days later, support starts receiving complaints. Customers say the agent is giving wrong information about return deadlines.

**What happened?** By changing the tone, you inadvertently also changed the agent's behavior. But you had no way of knowing — because you weren't comparing against a fixed baseline.

This problem has a name: **regression**. And the solution is an **evaluation dataset**.

---

### What is an Evaluation Dataset?

It's a fixed collection of `question → expected answer` pairs that represents your agent's correct behavior. It doesn't change — it's your quality "ruler".

```python
DATASET = [
    {
        "question": "What is the return deadline?",
        "expected_answer": "The return deadline is 30 days after purchase."
    },
    {
        "question": "How do I track my delivery?",
        "expected_answer": "Access the website with the tracking code sent by email."
    },
]
```

Every time you change something in the agent (prompt, model, tools), you run the agent on the same dataset and compare scores:

```
prompt v1 → average score: 0.85  ✅
prompt v2 → average score: 0.60  ⚠️ REGRESSION DETECTED
```

With this, you detect the problem **before** deploying — not after receiving complaints.

---

### 🎯 Objective

Create a fixed dataset of 5 questions with expected answers, run the agent with 2 different prompt versions, and use an LLM-as-a-Judge to detect which version caused regression.

---

### 🛠️ What to Build

**1. Fixed dataset:**
```python
DATASET = [
    {"question": "...", "expected_answer": "..."},
    # 5 items total — you define the theme (e-commerce, tech support, etc.)
]
```

**2. Similarity judge** — evaluates how close the agent's response is to the expected answer:
```
Score 1.0 → correct and complete answer
Score 0.5 → partially correct
Score 0.0 → incorrect or contradicts expected answer
```

**3. Two prompt variations** to compare:
```python
VARIATIONS = [
    {"name": "formal", "system_prompt": "Respond in a formal and technical manner."},
    {"name": "casual", "system_prompt": "Respond in a casual and friendly manner."},
]
```

**4. Log to MLflow:**
- `average_judge_score` per variation
- `judge_per_question` with step (to see which question regressed)

---

### 🎁 Bonus
Register the dataset in Langfuse using `langfuse.api.datasets.create()` and link each execution to a dataset item.

---

## Exercise 4 — Latency and Quality Monitor

### 📖 Context

Your agent is in production. Everything seems fine — but "seems" isn't enough. You need data.

Think about how web server monitoring works: nobody watches the dashboard 24 hours a day. Instead, you configure **alerts** — if the server takes more than 2 seconds to respond, or if the error rate exceeds 1%, you get a notification.

With LLM agents, the logic is the same. Only the indicators are different:

- **Latency** → how long the agent takes to respond
- **Quality** → is the judge score dropping?
- **Cost** → are tokens increasing for no reason?

If any of these indicators goes out of normal range, you want to know **now** — not at next Monday's meeting.

---

### What are Thresholds?

A threshold is the value at which something becomes a problem. You define it based on your SLA (service level agreement) or system experience.

Examples:
```
latency > 3s        → user starts to give up
judge score < 0.6   → quality below acceptable
total_tokens > 2000 → cost above expected per question
```

When a threshold is violated, you trigger an **alert** — which can be a log, an email, a Slack message, or a PagerDuty in critical cases.

---

### 🎯 Objective

Add a monitoring system to the agent that automatically detects when latency or quality are out of expected range, logs alerts, and exposes them as metrics in MLflow.

---

### 🛠️ What to Build

**1. Configurable thresholds:**
```python
THRESHOLDS = {
    "max_latency_seconds": 3.0,
    "min_judge_score": 0.6,
    "max_tokens_per_response": 1500,
}
```

**2. Verification function after each response:**
```python
def check_alerts(metrics: dict, thresholds: dict) -> list[str]:
    alerts = []
    if metrics["latency_seconds"] > thresholds["max_latency_seconds"]:
        alerts.append(f"⚠️ HIGH LATENCY: {metrics['latency_seconds']}s")
    if metrics["judge_score"] < thresholds["min_judge_score"]:
        alerts.append(f"⚠️ LOW QUALITY: score {metrics['judge_score']}")
    return alerts
```

**3. Alert logging to file** (`alerts.log`):
```
2026-04-24 17:32:10 | HIGH LATENCY | 4.2s | question: "How do I cancel my order?"
2026-04-24 17:32:45 | LOW QUALITY | score 0.4 | question: "What is the delivery time?"
```

**4. Log to MLflow:**
- `alerts_triggered` (total alerts in run)
- `latency_alerts` and `quality_alerts` separately

---

### 🎁 Bonus
Simulate a Slack alert by printing the formatted message to terminal:
```
🚨 [SLACK ALERT] #agent-monitoring
High latency detected: 4.2s (threshold: 3.0s)
Question: "How do I cancel my order?"
MLflow Run: agent-1745510400
```

---

## Exercise 5 — Automated Experiment Report

### 📖 Context

You ran your experiments, collected metrics, and now need to present results to the product team. The CTO wants a clear recommendation: **which model to use in production?**

You could open MLflow and take screenshots. But that's not scalable — and not what a production engineer does.

In mature ML teams, the experiment report is **automatically generated** at the end of each test round. It includes comparative tables, charts, and a data-based recommendation. The engineer reviews and approves — but doesn't write from scratch.

This has a name: **MLOps**. And what you'll build in this exercise is a simplified version of this pipeline.

---

### Why does the LLM generate the recommendation?

Because the LLM is good at synthesizing data and writing structured text. Instead of you writing:

> *"The claude-haiku-4-5 model showed average latency of 1.2s and judge score of 0.82, while claude-opus-4-5 showed latency of 3.4s and judge score of 0.91. Considering cost-benefit..."*

You pass the data to the LLM and it writes this for you — based on actual experiment numbers.

```python
prompt = f"""
You are a senior ML engineer. Analyze the results below and write
a 2-paragraph recommendation about which model to use in production.

Experiment data:
{json.dumps(results, indent=2)}

Decision criteria: quality (judge score) has 60% weight, cost (tokens) has 40% weight.
"""
```

---

### 🎯 Objective

Run 3 experiment variations (model or prompt), collect metrics, and automatically generate a complete Markdown report with comparative table, bar chart, and LLM-written recommendation.

---

### 🛠️ What to Build

**1. Run 3 variations** (you choose — models, prompts, or temperatures)

**2. Generate comparative table in Markdown:**
```markdown
| Model | Avg Tokens | Avg Latency | Judge Score |
|-------|-----------|-------------|-------------|
| haiku | 450       | 1.2s        | 0.82        |
| opus  | 890       | 3.4s        | 0.91        |
```

**3. Generate bar chart** with matplotlib comparing `average_judge_score` per variation and save as `chart.png`

**4. Generate recommendation with LLM** — pass data as JSON and ask for written analysis

**5. Save everything to `report.md`:**
```markdown
# Experiment Report — 2026-04-24

## Results
[table]

## Analysis
[LLM-generated text]
```

---

### 🎁 Bonus
Add a **risks** section to the report — ask the LLM to identify potential problems with the recommended option:
```
## Recommendation Risks
[LLM analyzes trade-offs and points out what could go wrong]
```

---

## General Tips

For all 3 exercises, the `Example3_mlflow/example_mlflow.py` file we already have is the starting point. The base structure doesn't change — what changes is what you do **with the results** after each run.

Suggested implementation order:
1. Make the agent run and collect metrics
2. Add the judge
3. Add the new feature for the exercise (regression / alerts / report)
4. Test by forcing edge cases (sleep for latency, bad prompt for low quality)

---

## 🎓 Learning Objectives

These exercises teach:

1. **Regression Detection**: How to prevent quality degradation in production
2. **Evaluation Datasets**: Building and maintaining quality baselines
3. **Production Monitoring**: Real-time alerting for latency and quality issues
4. **Threshold Management**: Setting and enforcing SLA boundaries
5. **Automated Reporting**: MLOps practices for experiment documentation
6. **LLM-Generated Analysis**: Using LLMs to synthesize experiment results

---

## 🚀 Success Criteria

### Exercise 3 (Regression Detection)
- ✅ Fixed dataset with 5 question-answer pairs
- ✅ Similarity judge scoring responses
- ✅ Two prompt variations tested
- ✅ Regression detected and logged to MLflow
- 🎁 Dataset registered in Langfuse

### Exercise 4 (Monitoring)
- ✅ Configurable thresholds for latency, quality, cost
- ✅ Alert detection after each response
- ✅ Alerts logged to file with timestamps
- ✅ Alert metrics in MLflow
- 🎁 Slack-formatted alert messages

### Exercise 5 (Automated Report)
- ✅ 3 variations tested and compared
- ✅ Markdown table with comparative metrics
- ✅ Bar chart visualization saved as PNG
- ✅ LLM-generated recommendation
- ✅ Complete report saved to `report.md`
- 🎁 Risk analysis section

---

## 📚 Additional Resources

- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- [Langfuse Datasets](https://langfuse.com/docs/datasets)
- [SLA Best Practices](https://sre.google/sre-book/service-level-objectives/)
- [MLOps Principles](https://ml-ops.org/)

---

## 🔥 Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Dataset too small | Use at least 10-20 examples for reliable regression detection |
| Thresholds too strict | Start loose, tighten based on actual production data |
| No baseline metrics | Run experiments before setting thresholds |
| Ignoring false positives | Review alerts regularly and adjust thresholds |
| Manual report generation | Automate from day one, even if simple |
