# 🔍 Observability Module

This module demonstrates how to implement **observability** in AI agents using industry-standard tools: **Langfuse** (cloud) and **MLflow** (local).

---

## 🎯 Objective

Learn how to monitor, trace, and analyze AI agent behavior in production by:

- Tracking LLM calls and token usage
- Monitoring tool executions
- Measuring latency and performance
- Analyzing conversation flows
- Debugging agent behavior

---

## 🧱 Architecture

```
Agent → Anthropic Claude API
  ↓
  ├─→ Langfuse (Cloud) - Traces, sessions, metadata
  └─→ MLflow (Local)   - Metrics, parameters, experiments
```

---

## 📊 What Gets Tracked

### Langfuse (Cloud Tracing)
- **Traces**: Complete execution flow of each agent run
- **Sessions**: Group related conversations
- **Metadata**: Model version, session IDs, custom attributes
- **Tool calls**: Individual function executions with inputs/outputs

### MLflow (Local Metrics)
- **Parameters**: Model name, user message, session ID
- **Metrics**: 
  - Input/output tokens
  - Total tokens consumed
  - Number of tool calls
  - Iterations count
  - Latency (seconds)
- **Experiments**: Organized runs for comparison

---

## ⚙️ Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- API Keys:
  - `ANTHROPIC_API_KEY` (Claude) - [Get it here](https://console.anthropic.com/settings/keys)
  - `LANGFUSE_PUBLIC_KEY` (Langfuse) - [Get it here](https://cloud.langfuse.com/settings)
  - `LANGFUSE_SECRET_KEY` (Langfuse)
  - Optional: `OPENAI_API_KEY` (GPT models) - [Get it here](https://platform.openai.com/api-keys)
  - Optional: `GEMINI_API_KEY` (Gemini models) - [Get it here](https://makersuite.google.com/app/apikey)

### 1. Install Dependencies

```bash
pip install anthropic langfuse mlflow python-dotenv
```

### 2. Configure Environment Variables

Copy the example environment file and add your API keys:

```bash
cd examples_exercises/observability
cp .env.example .env
```

Edit `.env` and add your actual API keys:

```env
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
LANGFUSE_PUBLIC_KEY=pk-lf-your-actual-public-key-here
LANGFUSE_SECRET_KEY=sk-lf-your-actual-secret-key-here
LANGFUSE_HOST=https://cloud.langfuse.com
```

**Important**: Never commit your `.env` file to version control!

### 3. Start MLflow Server

```bash
cd examples_exercises/observability
docker compose up -d
```

This starts MLflow on `http://localhost:5001`

### 4. Run the Examples

```bash
cd Example1
python agent1.py
```

---

## 🔧 Available Tools

The example agent includes three tools:

### 1. Calculator
Performs basic math operations: add, subtract, multiply, divide

**Example**: "What is 1234 multiplied by 56, divided by 7?"

### 2. Get Current Time
Returns current date and time

**Example**: "What time is it now?"

### 3. Text Analyzer
Analyzes text and returns statistics (words, characters, sentences)

**Example**: "Analyze this text: 'Today is a beautiful sunny day. The sky is blue!'"

---

## 📈 Viewing Results

### MLflow Dashboard
1. Open browser: `http://localhost:5001`
2. Navigate to "Experiments" → "agente-claude"
3. View metrics, parameters, and compare runs

### Langfuse Dashboard
1. Login to [Langfuse Cloud](https://cloud.langfuse.com)
2. View traces, sessions, and detailed execution flows
3. Analyze token usage and costs

---

## 🧪 Example Queries

### Example 1

The example script includes two test queries:

1. **Math with steps**: "What is 1234 multiplied by 56, divided by 7? Show me step by step."
   - Demonstrates: Multiple tool calls, reasoning chain

2. **Multi-tool**: "What time is it now? Also analyze this text: 'Today is a beautiful sunny day. The sky is blue!'"
   - Demonstrates: Multiple different tools in one query

### Example 2 (LLM-as-a-Judge)

The example includes three test queries designed to evaluate tool usage:

1. **Math Query**: "What is 1234 multiplied by 56, divided by 7?"
   - Expected: Should use calculator tool
   - Judge evaluates: Correct tool selection

2. **Time Query**: "What time is it now?"
   - Expected: Should use get_current_time tool
   - Judge evaluates: Appropriate tool usage

3. **Knowledge Query**: "What is the capital of France?"
   - Expected: Should NOT use tools (direct answer)
   - Judge evaluates: Avoiding unnecessary tool calls

### Example 3 (A/B Testing)

The example compares three temperature values (0.0, 0.5, 1.0) using two test queries:

1. **Creative Task**: "Create a creative metaphor to explain what artificial intelligence is."
   - Tests: Creativity variation across temperatures
   - Metrics: Response length, token usage, consistency

2. **Summarization Task**: "Summarize in one sentence: 'The sky is blue because air molecules scatter blue light more than other colors.'"
   - Tests: Conciseness and consistency
   - Metrics: Token efficiency, response quality

---

## 🎓 Learning Objectives

This module teaches:

1. **Instrumentation**: How to add observability to agent code using decorators (`@observe()`)
2. **Metrics tracking**: What metrics matter for AI agents
3. **Debugging**: How to trace execution flow and identify issues
4. **Performance**: How to measure and optimize latency
5. **Cost monitoring**: Track token usage and API costs
6. **Quality evaluation**: Use LLM-as-a-Judge to automatically evaluate agent behavior
7. **Automated scoring**: Implement quantitative quality metrics
8. **A/B Testing**: Systematically compare different agent configurations
9. **Experimentation**: Design and run controlled experiments with MLflow
10. **Regression detection**: Prevent quality degradation with evaluation datasets
11. **Production monitoring**: Real-time alerting for SLA violations
12. **Automated reporting**: MLOps practices for experiment documentation

---

## 🔥 Common Issues

| Issue | Solution |
|---|---|
| MLflow not accessible | Check if container is running: `docker ps` |
| Langfuse not tracking | Verify API keys in `.env` file |
| Port 5001 occupied | Change port in `docker-compose.yml`: `"5002:5000"` |
| Missing dependencies | Run `pip install -r requirements.txt` |

---

## 📚 Additional Resources

- [Langfuse Documentation](https://langfuse.com/docs)
- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [Anthropic SDK](https://docs.anthropic.com/en/api/client-sdks)

---

---

## 📁 Examples

### Example 1: Basic Observability
- Simple agent with Langfuse + MLflow integration
- Tracks tokens, latency, tool calls
- Foundation for observability

[View Example 1 →](./Example1/)

### Example 2: LLM-as-a-Judge
- Extends Example 1 with automated quality evaluation
- Uses LLM to evaluate tool usage correctness
- Scores sent to Langfuse and MLflow
- Demonstrates quality monitoring patterns

[View Example 2 →](./Example2/)

### Example 3: A/B Testing & Experimentation
- Systematic comparison of agent configurations
- Temperature, model, and parameter optimization
- Fair comparison with consistent test sets
- MLflow experiments for reproducible results

[View Example 3 →](./Example3_mlflow/)

### 🏆 Challenge: Production Implementation
- Advanced exercises for production-ready monitoring
- **Exercise 3**: Regression detection with evaluation datasets
- **Exercise 4**: Real-time latency and quality monitoring with alerts
- **Exercise 5**: Automated experiment reports with LLM-generated analysis

[View Challenge →](./Challenge/)

---

## 🚀 Next Steps

After understanding these examples:

1. Add custom metrics for your use case
2. Implement error tracking and alerting
3. Create dashboards for production monitoring
4. Set up cost budgets and alerts
5. Analyze user behavior patterns
6. Implement LLM-as-a-Judge for quality monitoring
7. Build evaluation datasets for regression testing
8. Run A/B tests to optimize agent parameters
9. Set up continuous experimentation pipelines
10. Implement statistical significance testing for experiments
11. **Complete the Challenge exercises** for production-ready implementations

---

## 🏗️ Module Structure

```
observability/
├── README.md                    # Module overview
├── docker-compose.yml           # MLflow setup
├── Example1/                    # Basic observability
│   ├── agent1.py
│   └── README.md
├── Example2/                    # LLM-as-a-Judge
│   ├── agent2.py
│   └── README.md
├── Example3_mlflow/             # A/B Testing
│   ├── example_mlflow.py
│   └── README.md
└── Challenge/                   # Production exercises
    └── README.md
```
