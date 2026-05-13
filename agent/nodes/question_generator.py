"""
Question Generator node.

Uses the LLM to identify gaps or ambiguities in the portal context analysis
and generates clarifying questions for the user. Uses LangGraph's interrupt()
to pause execution and wait for user input.
"""

from __future__ import annotations

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import interrupt

from agent.prompts.templates import QUESTION_GENERATION_PROMPT, SYSTEM_PROMPT
from agent.state import AgentState
from utils.logger import setup_logger

logger = setup_logger("question_generator")


def create_question_generator(llm: BaseChatModel):
    """Factory that creates the question_generator node with the given LLM."""

    def question_generator(state: AgentState) -> dict:
        """
        Identify gaps and ask the user clarifying questions.
        Pauses the graph via interrupt() until the user answers.
        """
        analysis = state.get("analysis")
        documents = state.get("documents", [])

        if not analysis:
            return {"error": "No analysis available to generate questions from.", "phase": "error"}

        doc_names = ", ".join(d.get("filename", "Unknown") for d in documents)

        prompt = QUESTION_GENERATION_PROMPT.format(
            analysis=analysis,
            document_names=doc_names,
        )

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]

        try:
            # 1. Ask LLM to generate questions
            logger.info("Invoking LLM to generate clarifying questions...")
            response = llm.invoke(messages)
            questions_text = response.content

            # Parse the text into a list of questions (simple split by newline for now)
            # In a real app, you might want structured output here too, but raw text is fine
            # for displaying in a chat interface.
            questions = [q.strip() for q in questions_text.split("\n") if q.strip()]
            
            logger.info(f"Generated {len(questions)} questions.")

            # 2. Pause execution and ask the user
            # The payload we pass to interrupt() is what the UI will see
            logger.info("Interrupting graph execution to ask user for clarifications.")
            user_response = interrupt({
                "action": "ask_user",
                "questions": questions,
                "raw_text": questions_text,
                "message": "I need some clarifications before generating the final JSON.",
            })

            # 3. When resumed, user_response contains the user's answers
            # user_response will be the payload passed to Command(resume=...)
            answers = user_response.get("answers", [])
            raw_answers = user_response.get("raw_text", "No answers provided.")
            
            logger.info("Resumed graph execution with user answers.")

            return {
                "questions": questions,
                "user_answers": answers,
                "phase": "generating",
                "messages": [
                    response,
                    HumanMessage(content=f"User's answers to your questions:\n{raw_answers}"),
                ],
            }

        except Exception as e:
            logger.exception(f"Question generation failed: {str(e)}")
            return {
                "error": f"Question generation failed: {str(e)}",
                "phase": "error",
            }

    return question_generator
