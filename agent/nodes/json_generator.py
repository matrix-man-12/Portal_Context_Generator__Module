"""
JSON Generator node.

Takes the combined analysis and user answers, and uses the LLM
to generate the final structured JSON conforming to the Pydantic schema.
"""

from __future__ import annotations

import json
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

from agent.prompts.templates import JSON_GENERATION_PROMPT, SYSTEM_PROMPT
from agent.state import AgentState
from schemas.portal_schema import GeneratedOutput


def create_json_generator(llm: BaseChatModel):
    """Factory that creates the json_generator node with the given LLM."""

    # Bind the structured output schema to the LLM
    structured_llm = llm.with_structured_output(GeneratedOutput)

    def json_generator(state: AgentState) -> dict:
        """
        Generate structured JSON from the analysis and user answers.
        """
        analysis = state.get("analysis")
        documents = state.get("documents", [])
        
        # We might not have user answers if the LLM didn't ask questions
        user_answers = state.get("user_answers", [])
        clarifications = "\n".join(user_answers) if user_answers else "None provided."

        if not analysis:
            return {"error": "No analysis available to generate JSON from.", "phase": "error"}

        doc_names = ", ".join(d.get("filename", "Unknown") for d in documents)

        prompt = JSON_GENERATION_PROMPT.format(
            analysis=analysis,
            clarifications=clarifications,
            document_names=doc_names,
        )

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        try:
            # Generate the structured output
            output: GeneratedOutput = structured_llm.invoke(messages)

            # Store the resulting data in the state
            portal_info_dict = output.get_portal_info_dict()
            workflows = [wf.model_dump(mode="json") for wf in output.workflows]

            return {
                "portal_context": portal_info_dict,
                "workflows": workflows,
                "phase": "review",
                "iteration": state.get("iteration", 0) + 1,
            }

        except Exception as e:
            return {
                "error": f"JSON generation failed: {str(e)}",
                "phase": "error",
            }

    return json_generator
