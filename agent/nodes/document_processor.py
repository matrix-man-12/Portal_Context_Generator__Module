"""
Document Processor node.

Takes parsed documents from the state and consolidates them into a
single formatted text block ready for LLM analysis.
"""

from __future__ import annotations

from agent.state import AgentState


def document_processor(state: AgentState) -> dict:
    """
    Consolidate parsed documents into a single text block for LLM consumption.

    This node doesn't call the LLM — it just formats the documents.
    The heavy LLM work happens in context_builder.
    """
    documents = state.get("documents", [])

    if not documents:
        return {
            "phase": "error",
            "error": "No documents uploaded. Please upload at least one document.",
        }

    # Build consolidated document text
    doc_parts = []
    for i, doc in enumerate(documents, 1):
        filename = doc.get("filename", f"Document {i}")
        file_type = doc.get("file_type", "unknown")
        content = doc.get("content", "")
        char_count = len(content)

        doc_parts.append(
            f"{'='*60}\n"
            f"DOCUMENT {i}: {filename} (type: {file_type}, {char_count} chars)\n"
            f"{'='*60}\n"
            f"{content}\n"
        )

    consolidated = "\n\n".join(doc_parts)

    # Truncate if too long (rough limit for context window safety)
    MAX_CHARS = 200_000
    if len(consolidated) > MAX_CHARS:
        consolidated = consolidated[:MAX_CHARS] + (
            f"\n\n[TRUNCATED — original content was {len(consolidated)} chars, "
            f"showing first {MAX_CHARS}]"
        )

    return {
        "documents": documents,  # Pass through unchanged
        "analysis": None,  # Will be filled by context_builder
        "phase": "analyzing",
    }


def get_consolidated_docs_text(state: AgentState) -> str:
    """
    Helper to rebuild the consolidated document text from state.
    Used by downstream nodes that need the raw document content.
    """
    documents = state.get("documents", [])
    parts = []
    for i, doc in enumerate(documents, 1):
        filename = doc.get("filename", f"Document {i}")
        content = doc.get("content", "")
        parts.append(f"### Document: {filename}\n{content}")

    text = "\n\n".join(parts)

    MAX_CHARS = 200_000
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS] + "\n\n[TRUNCATED]"

    return text
