# LLM Configuration

The Portal Context Generator supports multiple LLM providers, making it adaptable to different environments—from cloud-hosted models to completely air-gapped, local setups.

## Supported Providers

We currently support three provider types:
1. **Google Gemini** (Default model: `gemini-2.5-flash`)
2. **Anthropic Claude** (Default model: `claude-sonnet-4-20250514`)
3. **Local (OpenAI-compatible)**

### Local LLMs (OpenAI Compatible)
For local privacy and execution, the system can connect to local servers like **LM Studio** or **Ollama** that expose an OpenAI-compatible API endpoint.
- **Base URL**: e.g., `http://localhost:1234/v1` for LM Studio.
- **Model Name**: The exact name of the model loaded in the local server (e.g., `meta-llama-3-8b-instruct`).
- **API Key**: Usually left blank or as `"not-needed"`, depending on the server requirements.

## How It Works (`utils/helpers.py`)

The `create_llm` factory function initializes the appropriate LangChain `BaseChatModel`:

```python
def create_llm(provider, api_key, model_name=None, base_url=None, temperature=0.3):
    # Initializes ChatGoogleGenerativeAI, ChatAnthropic, or ChatOpenAI
    ...
```

**Temperature**: Hardcoded to `0.3` across all providers. A lower temperature reduces hallucinations and ensures the LLM closely adheres to the structured JSON schemas.

## Connection Testing
Before the LangGraph agent is initialized, the UI runs a connection test `test_llm_connection()`. It sends a simple `"Say 'OK' if you can hear me."` prompt to verify that API keys are valid and that local servers are running. If this fails, the user is presented with a clear error message in the UI and the agent is not started.
