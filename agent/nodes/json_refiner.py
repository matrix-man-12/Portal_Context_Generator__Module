"""
JSON Refiner node.

Allows the user to request changes to the generated JSON.
Takes user feedback and applies it to the existing JSON using structured output.
Uses interrupt() to pause and present the JSON for review.
"""

from __future__ import annotations

import json
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import interrupt

from agent.prompts.templates import JSON_REFINEMENT_PROMPT, SYSTEM_PROMPT
from agent.state import AgentState
from schemas.portal_schema import GeneratedOutput, PortalContext, Workflow
from utils.logger import setup_logger

logger = setup_logger("json_refiner")


def create_json_refiner(llm: BaseChatModel):
    """Factory that creates the json_refiner node with the given LLM."""

    structured_llm = llm.with_structured_output(GeneratedOutput)

    def json_refiner(state: AgentState) -> dict:
        """
        Review JSON and refine based on feedback.
        Pauses the graph via interrupt() to let the user review the JSON.
        """
        portal_context = state.get("portal_context")
        workflows = state.get("workflows", [])

        if not portal_context:
            return {"error": "No JSON available to refine.", "phase": "error"}

        # Combine into a single representation for the prompt
        current_json_obj = {
            "portal_context": portal_context,
            "workflows": workflows
        }
        current_json_str = json.dumps(current_json_obj, indent=2)

        # 1. Pause execution and present JSON for review
        logger.info("Interrupting graph execution to allow user to review the generated JSON.")
        user_response = interrupt({
            "action": "review_json",
            "portal_context": portal_context,
            "workflows": workflows,
            "message": "Please review the generated portal context. You can approve it or request changes.",
        })

        # 2. When resumed, check if approved or if changes requested
        action = user_response.get("action")
        
        if action == "approve":
            logger.info("User approved the generated JSON. Graph complete.")
            # Flow goes to END
            return {
                "phase": "complete",
            }
            
        elif action == "refine":
            # User wants changes
            feedback = user_response.get("feedback", "No specific feedback provided.")
            
            prompt = JSON_REFINEMENT_PROMPT.format(
                current_json=current_json_str,
                feedback=feedback,
            )

            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ]

            try:
                # Ask LLM to apply changes and output the new structured JSON
                logger.info("Invoking LLM to refine JSON based on user feedback...")
                output: GeneratedOutput = structured_llm.invoke(messages)

                portal_info_dict = output.get_portal_info_dict()
                new_workflows = [wf.model_dump(mode="json") for wf in output.workflows]
                
                logger.info("JSON refinement successful.")

                return {
                    "portal_context": portal_info_dict,
                    "workflows": new_workflows,
                    "feedback": feedback,
                    "iteration": state.get("iteration", 0) + 1,
                    # We keep phase="review" so it will loop back to the interrupt
                    "phase": "review",
                }

            except Exception as e:
                logger.exception(f"JSON refinement failed: {str(e)}")
                return {
                    "error": f"JSON refinement failed: {str(e)}",
                    "phase": "error",
                }
                
        else:
            return {"error": f"Unknown review action: {action}", "phase": "error"}

    return json_refiner
