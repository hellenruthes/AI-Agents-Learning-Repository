# 🔐 Setup Guide: API Keys and Credentials

This guide walks you through obtaining and configuring all necessary API keys for the observability examples.

---

## 📋 Required API Keys

### 1. Anthropic API Key (Required)

**What it's for**: Access to Claude models (claude-haiku-4-5, claude-sonnet-4-5, claude-opus-4-5)

**How to get it**:
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to **Settings** → **API Keys**
4. Click **Create Key**
5. Copy the key (starts with `sk-ant-`)

**Pricing**: Pay-as-you-go based on tokens used
- Haiku: ~$0.25 per million input tokens
- Sonnet: ~$3 per million input tokens
- Opus: ~$15 per million input tokens

---

### 2. Langfuse Keys (Required)

**What it's for**: Observability platform for tracing, monitoring, and analyzing LLM applications

**How to get it**:
1. Go to [Langfuse Cloud](https://cloud.langfuse.com/)
2. Sign up for a free account
3. Create a new project
4. Navigate to **Settings** → **API Keys**
5. Copy both keys:
   - **Public Key** (starts with `pk-lf-`)
   - **Secret Key** (starts with `sk-lf-`)

**Pricing**: Free tier available (50k observations/month)

---

## 🔧 Optional API Keys

### 3. OpenAI API Key (Optional)

**What it's for**: Access to GPT models (GPT-4, GPT-3.5-turbo, etc.)

**How to get it**:
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **Create new secret key**
5. Copy the key (starts with `sk-`)

**Note**: This is the same key used for ChatGPT API access

**Pricing**: Pay-as-you-go
- GPT-4: ~$30 per million input tokens
- GPT-3.5-turbo: ~$0.50 per million input tokens

---

### 4. Google Gemini API Key (Optional)

**What it's for**: Access to Gemini models (gemini-pro, gemini-pro-vision)

**How to get it**:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API Key**
4. Copy the key

**Pricing**: Free tier available (60 requests per minute)

---

## 🛠️ Configuration Steps

### Step 1: Copy the Example File

```bash
cd examples_exercises/observability
cp .env.example .env
```

### Step 2: Edit the .env File

Open `.env` in your text editor and replace the placeholder values:

```env
# Required
ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key-here
LANGFUSE_PUBLIC_KEY=pk-lf-your-actual-public-key-here
LANGFUSE_SECRET_KEY=sk-lf-your-actual-secret-key-here
LANGFUSE_HOST=https://cloud.langfuse.com

# Optional (only if using these models)
OPENAI_API_KEY=sk-your-actual-openai-key-here
GEMINI_API_KEY=your-actual-gemini-key-here
```

### Step 3: Verify Configuration

Run this test script to verify your keys are working:

```python
# test_credentials.py
import os
from dotenv import load_dotenv
import anthropic
from langfuse import Langfuse

load_dotenv()

# Test Anthropic
try:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    print("✅ Anthropic API key is valid")
except Exception as e:
    print(f"❌ Anthropic API key error: {e}")

# Test Langfuse
try:
    langfuse = Langfuse()
    print("✅ Langfuse keys are valid")
except Exception as e:
    print(f"❌ Langfuse keys error: {e}")
```

Run it:
```bash
python test_credentials.py
```

---

## 🔒 Security Best Practices

### ✅ DO:
- Keep your `.env` file local (it's already in `.gitignore`)
- Use different API keys for development and production
- Rotate keys regularly
- Set up billing alerts on provider platforms
- Use environment-specific keys in CI/CD

### ❌ DON'T:
- Commit `.env` files to version control
- Share API keys in chat, email, or screenshots
- Use production keys in development
- Hard-code keys in source code
- Store keys in plain text files outside `.env`

---

## 💰 Cost Management

### Set Up Billing Alerts

**Anthropic**:
1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Navigate to **Settings** → **Billing**
3. Set up usage alerts

**OpenAI**:
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Navigate to **Settings** → **Billing** → **Usage limits**
3. Set monthly budget caps

### Estimate Costs

For the examples in this module:

| Example | Estimated Tokens | Estimated Cost (Claude Haiku) |
|---------|------------------|-------------------------------|
| Example 1 | ~2,000 tokens | ~$0.001 |
| Example 2 | ~3,000 tokens | ~$0.002 |
| Example 3 | ~6,000 tokens | ~$0.003 |
| Challenge | ~10,000 tokens | ~$0.005 |

**Total**: Less than $0.02 to run all examples

---

## 🆘 Troubleshooting

### "API key not found" error

**Solution**: Make sure you're running commands from the correct directory and `.env` file exists:
```bash
ls -la .env  # Should show the file
cat .env     # Should show your keys (be careful not to share output!)
```

### "Invalid API key" error

**Solution**: 
1. Verify the key is copied correctly (no extra spaces)
2. Check if the key is active in the provider's console
3. Regenerate the key if needed

### Langfuse connection timeout

**Solution**:
1. Check your internet connection
2. Verify `LANGFUSE_HOST` is set to `https://cloud.langfuse.com`
3. Check Langfuse status at [status.langfuse.com](https://status.langfuse.com)

### Rate limit errors

**Solution**:
1. Add delays between requests: `time.sleep(1)`
2. Use exponential backoff for retries
3. Upgrade to higher tier if needed

---

## 🔄 Self-Hosted Langfuse (Advanced)

If you prefer to run Langfuse locally instead of using the cloud version:

### 1. Start Langfuse with Docker

```bash
# In the observability directory
docker compose -f docker-compose-langfuse.yml up -d
```

### 2. Update .env

```env
LANGFUSE_HOST=http://localhost:3000
LANGFUSE_PUBLIC_KEY=your-local-public-key
LANGFUSE_SECRET_KEY=your-local-secret-key
```

### 3. Access Langfuse UI

Open `http://localhost:3000` and create your API keys in the settings.

---

## 📚 Additional Resources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Langfuse Documentation](https://langfuse.com/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Google AI Studio Documentation](https://ai.google.dev/docs)

---

## ✅ Checklist

Before running the examples, make sure you have:

- [ ] Created `.env` file from `.env.example`
- [ ] Added Anthropic API key
- [ ] Added Langfuse public and secret keys
- [ ] (Optional) Added OpenAI API key
- [ ] (Optional) Added Gemini API key
- [ ] Verified keys with test script
- [ ] Set up billing alerts
- [ ] Started MLflow with `docker compose up -d`

You're ready to go! 🚀
