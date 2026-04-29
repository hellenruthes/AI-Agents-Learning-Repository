# 🧪 Example 3: A/B Testing and Experimentation with MLflow

This example demonstrates how to use **MLflow Experiments** to systematically compare different agent configurations and find optimal parameters.

---

## 🎯 Objective

Learn how to conduct controlled experiments with AI agents:

- **A/B Testing**: Compare different configurations side-by-side
- **Parameter Optimization**: Find the best temperature, model, or prompt
- **Fair Comparison**: Use the same test questions across all variations
- **Metric Tracking**: Measure performance, cost, and quality
- **Reproducibility**: Document and reproduce experiments

---

## 🆕 What's New in Example 3

### Systematic Experimentation

Instead of running the agent once, this example:

1. Defines **multiple variations** of a parameter (e.g., temperature: 0.0, 0.5, 1.0)
2. Runs **the same questions** through each variation
3. Tracks **metrics for each run** in MLflow
4. Enables **side-by-side comparison** in the MLflow UI

### Parameterized Agent

The agent is now fully parameterized:

```python
config = {
    "model": "claude-haiku-4-5",
    "temperature": 1.0,
    "max_tokens": 1024,
}
```

Easy to vary any parameter for experimentation.

### Aggregated Metrics

Tracks both:
- **Per-question metrics**: Individual performance
- **Average metrics**: Overall variation performance

---

## 🔬 Experiment Design

### Default Experiment: Temperature Comparison

The example compares three temperature values:

| Variation | Temperature | Expected Behavior |
|-----------|-------------|-------------------|
| 1 | 0.0 | Deterministic, consistent responses |
| 2 | 0.5 | Balanced creativity and consistency |
| 3 | 1.0 | Maximum creativity and variation |

### Test Questions

Two questions designed to test different aspects:

1. **Creative Task**: "Create a creative metaphor to explain what artificial intelligence is."
   - Tests: Creativity, variation across temperatures

2. **Summarization Task**: "Summarize in one sentence: 'The sky is blue because air molecules scatter blue light more than other colors.'"
   - Tests: Consistency, conciseness

---

## 📊 Metrics Tracked

### Per-Question Metrics
- `tokens_per_question`: Tokens used for each question
- `latency_per_question`: Response time for each question

### Aggregated Metrics
- `average_tokens`: Mean tokens across all questions
- `average_latency`: Mean latency across all questions
- `total_tool_calls`: Total tool invocations

### Parameters Logged
- `model`: Model name
- `temperature`: Temperature value
- `max_tokens`: Maximum tokens allowed

---

## 🚀 Running the Experiment

### Prerequisites

- MLflow running on `http://localhost:5001`
- Environment variables configured (`.env` file)

### Run

```bash
cd examples_exercises/observability/Example3_mlflow
python example_mlflow.py
```

### Expected Output

```
🧪 Experiment: temperature-comparison
   3 variations x 2 questions

============================================================
🔧 Variation: {'temperature': 0.0}
============================================================

  Question 1: Create a creative metaphor to explain what artificial...
  Response: Artificial intelligence is like a vast library where...
  Tokens: 245 | Latency: 1.23s

  Question 2: Summarize in one sentence: 'The sky is blue because...
  Response: Air molecules scatter blue light more than other colors.
  Tokens: 156 | Latency: 0.87s

============================================================
🔧 Variation: {'temperature': 0.5}
============================================================
...

✅ Experiment completed! View results at http://localhost:5001
```

---

## 📈 Analyzing Results in MLflow

### 1. Open MLflow UI

Navigate to `http://localhost:5001`

### 2. Select Experiment

Click on "temperature-comparison" experiment

### 3. Compare Runs

- View all three runs side-by-side
- Sort by metrics (e.g., lowest average_tokens)
- Compare parameters and outcomes

### 4. Visualize Metrics

- Click on a metric to see charts
- Compare trends across variations
- Identify optimal configuration

### 5. Key Questions to Answer

- **Cost**: Which temperature uses fewer tokens?
- **Speed**: Which temperature is fastest?
- **Consistency**: Which temperature gives most consistent results?
- **Quality**: Which temperature produces best responses? (requires manual review)

---

## 🔧 Customizing the Experiment

### Compare Different Parameters

#### Model Comparison

```python
EXPERIMENT_NAME = "model-comparison"

VARIATIONS = [
    {"model": "claude-haiku-4-5"},
    {"model": "claude-sonnet-4-5"},
    {"model": "claude-opus-4-5"},
]
```

#### Max Tokens Comparison

```python
EXPERIMENT_NAME = "max-tokens-comparison"

VARIATIONS = [
    {"max_tokens": 256},
    {"max_tokens": 512},
    {"max_tokens": 1024},
]
```

#### Multi-Parameter Comparison

```python
EXPERIMENT_NAME = "multi-param-comparison"

VARIATIONS = [
    {"model": "claude-haiku-4-5", "temperature": 0.0},
    {"model": "claude-haiku-4-5", "temperature": 1.0},
    {"model": "claude-sonnet-4-5", "temperature": 0.0},
    {"model": "claude-sonnet-4-5", "temperature": 1.0},
]
```

### Add More Test Questions

```python
QUESTIONS = [
    "Creative task question...",
    "Summarization task question...",
    "Reasoning task question...",
    "Code generation task question...",
]
```

### Add Custom Metrics

```python
# In run_agent function
result = {
    "response": final_text,
    "response_length": len(final_text),
    "unique_words": len(set(final_text.split())),
    # ... other metrics
}

# In run_experiment function
mlflow.log_metric("avg_response_length", total_response_length / n)
```

---

## 🎓 Learning Objectives

This example teaches:

1. **Experiment Design**: How to structure A/B tests for AI agents
2. **Fair Comparison**: Using consistent test sets across variations
3. **Metric Selection**: Choosing relevant metrics for comparison
4. **MLflow Experiments**: Using MLflow for systematic experimentation
5. **Parameter Optimization**: Finding optimal configurations
6. **Reproducibility**: Documenting experiments for future reference

---

## 💡 Best Practices

### Experiment Design

1. **Control Variables**: Change only one parameter at a time (unless testing interactions)
2. **Representative Questions**: Use questions that reflect real use cases
3. **Sufficient Sample Size**: Use enough questions for statistical significance
4. **Consistent Environment**: Run all variations in the same conditions

### Metric Selection

1. **Cost Metrics**: Tokens, API calls
2. **Performance Metrics**: Latency, throughput
3. **Quality Metrics**: Accuracy, relevance (may require human evaluation)
4. **Behavior Metrics**: Tool usage, reasoning steps

### Analysis

1. **Compare Averages**: Look at mean metrics across variations
2. **Check Variance**: High variance may indicate instability
3. **Consider Trade-offs**: Faster may mean lower quality, cheaper may mean less capable
4. **Manual Review**: Always review actual responses, not just metrics

---

## 🔥 Common Issues

| Issue | Solution |
|---|---|
| Runs not appearing in MLflow | Check MLflow server is running on port 5001 |
| Inconsistent results | Use temperature=0.0 for deterministic testing |
| High costs | Start with small question sets, use cheaper models |
| Can't compare runs | Ensure all runs use same experiment name |

---

## 📚 Additional Resources

- [MLflow Experiments Documentation](https://mlflow.org/docs/latest/tracking.html#organizing-runs-in-experiments)
- [A/B Testing Best Practices](https://www.optimizely.com/optimization-glossary/ab-testing/)
- [Statistical Significance Calculator](https://www.evanmiller.org/ab-testing/sample-size.html)

---

## 🚀 Next Steps

1. Run experiments comparing different models
2. Add quality evaluation metrics (LLM-as-a-Judge from Example 2)
3. Create automated experiment pipelines
4. Build dashboards for experiment results
5. Implement statistical significance testing
6. Set up continuous experimentation for production

---

## 🎯 Challenge Ideas

1. **Find Optimal Temperature**: Test temperatures from 0.0 to 1.0 in 0.1 increments
2. **Cost vs Quality**: Compare models and find the best cost/quality trade-off
3. **Prompt Engineering**: Test different system prompts
4. **Context Length**: Test different max_tokens values
5. **Multi-Objective**: Optimize for both speed and quality simultaneously
