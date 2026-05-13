"""
LangGraph definition for the Portal Context Generator.

Wires up the agent nodes, edges, and state persistence.
"""

from __future__ import annotations

import sqlite3
from langchain_core.language_models import BaseChatModel
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from agent.nodes.context_builder import create_context_builder
from agent.nodes.document_processor import document_processor
from agent.nodes.json_generator import create_json_generator
from agent.nodes.json_refiner import create_json_refiner
from agent.nodes.question_generator import create_question_generator
from agent.state import AgentState


def route_review(state: AgentState) -> str:
    """Conditional edge from json_refiner."""
    # If the user approved, phase is set to "complete"
    if state.get("phase") == "complete":
        return END
    # If they requested changes, phase is kept at "review"
    # and we loop back to the refiner to show them the new JSON
    return "json_refiner"


def build_graph(llm: BaseChatModel, db_path: str = "sessions.db"):
    """
    Build and compile the LangGraph agent.

    Args:
        llm: The initialized LangChain ChatModel.
        db_path: Path to the SQLite database for state persistence.

    Returns:
        The compiled graph ready for invocation.
    """
    builder = StateGraph(AgentState)

    # 1. Add nodes
    builder.add_node("document_processor", document_processor)
    builder.add_node("context_builder", create_context_builder(llm))
    builder.add_node("question_generator", create_question_generator(llm))
    builder.add_node("json_generator", create_json_generator(llm))
    builder.add_node("json_refiner", create_json_refiner(llm))

    # 2. Add edges
    builder.add_edge(START, "document_processor")
    builder.add_edge("document_processor", "context_builder")
    builder.add_edge("context_builder", "question_generator")
    builder.add_edge("question_generator", "json_generator")
    builder.add_edge("json_generator", "json_refiner")
    
    # Add conditional routing after refinement
    builder.add_conditional_edges(
        "json_refiner",
        route_review,
        {
            END: END,
            "json_refiner": "json_refiner", # Loop back to itself for another review
        }
    )

    # 3. Compile with checkpointer for state persistence
    conn = sqlite3.connect(db_path, check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    
    graph = builder.compile(checkpointer=checkpointer)
    
    return graph
