"""
Context Builder node.

Uses the LLM to analyze the consolidated documents and produce a
comprehensive understanding of the portal — its purpose, structure,
and available workflows.
"""

from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from agent.nodes.document_processor import get_consolidated_docs_text
from agent.prompts.templates import DOCUMENT_ANALYSIS_PROMPT, SYSTEM_PROMPT
from agent.state import AgentState


def create_context_builder(llm: BaseChatModel):
    """Factory that creates the context_builder node with the given LLM."""

    def context_builder(state: AgentState) -> dict:
        """
        Analyze documents with the LLM to extract portal context.

        Produces a detailed analysis that will be used by downstream nodes
        to generate questions and eventually the structured JSON.
        """
        docs_text = get_consolidated_docs_text(state)
        user_inputs = state.get("user_inputs", [])

        # Build user context section
        user_context = ""
        if user_inputs:
            user_context = "\n\nAdditional user-provided context:\n" + "\n".join(
                f"- {inp}" for inp in user_inputs
            )

        prompt = DOCUMENT_ANALYSIS_PROMPT.format(
            documents=docs_text,
            user_context=user_context,
        )

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        try:
            response = llm.invoke(messages)
            analysis = response.content

            return {
                "analysis": analysis,
                "phase": "questioning",
                "messages": [
                    HumanMessage(content="Analyze these portal documents."),
                    response,
                ],
            }
        except Exception as e:
            return {
                "error": f"LLM analysis failed: {str(e)}",
                "phase": "error",
            }

    return context_builder
