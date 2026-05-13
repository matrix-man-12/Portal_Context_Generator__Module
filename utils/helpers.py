"""
Shared utilities for the Portal Context Generator Module.

Includes:
- LLM provider factory (Gemini, Claude, Local/OpenAI-compatible)
- JSON file export helpers
- Miscellaneous formatting utilities
"""

from __future__ import annotations

import io
import json
import zipfile
from typing import Optional

from langchain_core.language_models import BaseChatModel

from utils.logger import setup_logger

logger = setup_logger("helpers")


# ---------------------------------------------------------------------------
# LLM Provider Factory
# ---------------------------------------------------------------------------

PROVIDER_GEMINI = "Google Gemini"
PROVIDER_CLAUDE = "Anthropic Claude"
PROVIDER_LOCAL = "Local (OpenAI-compatible)"

PROVIDER_CHOICES = [PROVIDER_GEMINI, PROVIDER_CLAUDE, PROVIDER_LOCAL]

# Default models per provider
DEFAULT_MODELS = {
    PROVIDER_GEMINI: "gemini-2.5-flash",
    PROVIDER_CLAUDE: "claude-sonnet-4-20250514",
    PROVIDER_LOCAL: "",  # User must specify
}


def create_llm(
    provider: str,
    api_key: str,
    model_name: Optional[str] = None,
    base_url: Optional[str] = None,
    temperature: float = 0.3,
) -> BaseChatModel:
    """
    Create an LLM instance based on the selected provider.

    Args:
        provider: One of PROVIDER_CHOICES.
        api_key: API key for the provider.
        model_name: Model name override. If None, uses default.
        base_url: Base URL for local/OpenAI-compatible LLMs.
        temperature: LLM temperature (default 0.3 for structured output).

    Returns:
        A LangChain BaseChatModel instance.

    Raises:
        ValueError: If the provider is unknown or required params are missing.
    """
    if provider == PROVIDER_GEMINI:
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=model_name or DEFAULT_MODELS[PROVIDER_GEMINI],
            google_api_key=api_key,
            temperature=temperature,
        )

    elif provider == PROVIDER_CLAUDE:
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            model=model_name or DEFAULT_MODELS[PROVIDER_CLAUDE],
            anthropic_api_key=api_key,
            temperature=temperature,
        )

    elif provider == PROVIDER_LOCAL:
        from langchain_openai import ChatOpenAI

        if not base_url:
            raise ValueError(
                "Base URL is required for local/OpenAI-compatible LLMs. "
                "Example: http://localhost:1234/v1"
            )
        if not model_name:
            raise ValueError(
                "Model name is required for local/OpenAI-compatible LLMs."
            )

        return ChatOpenAI(
            model=model_name,
            base_url=base_url,
            api_key=api_key or "not-needed",  # Some local LLMs don't need a key
            temperature=temperature,
        )

    else:
        raise ValueError(f"Unknown LLM provider: '{provider}'. Choose from: {PROVIDER_CHOICES}")


def test_llm_connection(llm: BaseChatModel) -> tuple[bool, str]:
    """
    Test the LLM connection with a simple prompt.

    Returns:
        (success: bool, message: str)
    """
    try:
        logger.info("Testing LLM connection...")
        response = llm.invoke("Say 'OK' if you can hear me.")
        logger.info("LLM connection test successful.")
        return True, f"Connected successfully. Response: {response.content[:100]}"
    except Exception as e:
        logger.error(f"LLM connection test failed: {str(e)}")
        return False, f"Connection failed: {str(e)}"


# ---------------------------------------------------------------------------
# JSON Export Helpers
# ---------------------------------------------------------------------------

def format_json(data: dict, indent: int = 2) -> str:
    """Pretty-format a dictionary as JSON string."""
    return json.dumps(data, indent=indent, ensure_ascii=False, default=str)


def create_zip_export(
    portal_info: dict,
    workflow_files: list[tuple[str, dict]],
) -> bytes:
    """
    Package portal info and workflow files into a ZIP archive.

    Args:
        portal_info: Portal info dictionary (for _portal_info.json).
        workflow_files: List of (filename, workflow_dict) tuples.

    Returns:
        ZIP file as bytes.
    """
    buffer = io.BytesIO()
    logger.info(f"Creating ZIP export with portal info and {len(workflow_files)} workflows.")
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # Write portal info
        zf.writestr(
            "_portal_info.json",
            format_json(portal_info),
        )
        # Write each workflow file
        for filename, wf_data in workflow_files:
            zf.writestr(filename, format_json(wf_data))

    buffer.seek(0)
    return buffer.getvalue()


def sanitize_filename(name: str) -> str:
    """Sanitize a string for use as a filename."""
    safe = name.lower().replace(" ", "_")
    safe = "".join(c for c in safe if c.isalnum() or c == "_")
    return safe
