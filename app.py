"""
Streamlit application entry point.
Provides the UI for the Portal Context Generator Module.
"""

import os
import uuid
from typing import Any

import streamlit as st
from langgraph.types import Command

from agent.graph import build_graph
from parsers.file_parser import get_supported_formats_display, parse_multiple_files
from utils.helpers import (
    PROVIDER_CHOICES,
    PROVIDER_GEMINI,
    PROVIDER_LOCAL,
    create_llm,
    create_zip_export,
    format_json,
    sanitize_filename,
    test_llm_connection,
)
from utils.logger import setup_logger

logger = setup_logger("app")


# ---------------------------------------------------------------------------
# Page Config & Session State Initialization
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Portal Context Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


def init_session_state():
    """Initialize Streamlit session state variables."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "graph" not in st.session_state:
        st.session_state.graph = None
    if "is_running" not in st.session_state:
        st.session_state.is_running = False
    if "current_interrupt" not in st.session_state:
        st.session_state.current_interrupt = None


init_session_state()

# ---------------------------------------------------------------------------
# Sidebar: Settings & LLM Configuration
# ---------------------------------------------------------------------------

with st.sidebar:
    st.header("⚙️ Configuration")

    # LLM Provider Selection
    provider = st.selectbox("LLM Provider", PROVIDER_CHOICES, index=0)

    api_key = st.text_input(
        f"API Key for {provider}",
        type="password",
        help="Leave blank if not required by your local LLM.",
    )

    model_name = ""
    base_url = ""

    if provider == PROVIDER_LOCAL:
        model_name = st.text_input(
            "Model Name",
            value="meta-llama-3-8b-instruct",
            help="Required for local LLMs.",
        )
        base_url = st.text_input(
            "Base URL",
            value="http://localhost:1234/v1",
            help="e.g., LM Studio local server URL.",
        )
    elif provider == PROVIDER_GEMINI:
        model_name = st.text_input(
            "Model Name (Optional)",
            value="gemini-2.5-flash",
            help="Leave as default or specify another Gemini model.",
        )

    # Initialize Graph Button
    if st.button("🔌 Connect & Initialize"):
        try:
            logger.info(f"Connecting to LLM provider: {provider}")
            with st.spinner("Connecting to LLM..."):
                llm = create_llm(
                    provider=provider,
                    api_key=api_key,
                    model_name=model_name if model_name else None,
                    base_url=base_url if base_url else None,
                )
                success, msg = test_llm_connection(llm)

                if success:
                    logger.info("Successfully connected to LLM.")
                    st.success("Connected!")
                    st.toast("LLM connection established!", icon="✅")
                    # Create the LangGraph agent
                    st.session_state.graph = build_graph(llm)
                    st.session_state.session_id = str(uuid.uuid4()) # Reset session on new connect
                    st.session_state.messages = []
                    st.session_state.current_interrupt = None
                else:
                    logger.error(f"Failed to connect to LLM: {msg}")
                    st.error(msg)
                    st.toast("LLM connection failed!", icon="❌")
        except Exception as e:
            logger.exception(f"Configuration Error: {str(e)}")
            st.error(f"Configuration Error: {str(e)}")
            st.toast("Configuration error occurred!", icon="⚠️")

    st.divider()
    st.markdown("### Session")
    st.text(f"ID: {st.session_state.session_id[:8]}...")
    if st.button("🔄 Reset Session"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.session_state.current_interrupt = None
        st.rerun()

# ---------------------------------------------------------------------------
# Main Layout
# ---------------------------------------------------------------------------

st.title("🤖 Portal Context Generator")
st.markdown(
    "Automate the extraction of UI workflows and actions from portal documentation "
    "into structured, automation-ready JSON."
)

if not st.session_state.graph:
    st.info("👈 Please configure and connect to an LLM provider in the sidebar to begin.")
    st.stop()

tab1, tab2, tab3 = st.tabs(["📄 1. Input & Upload", "💬 2. Agent Chat", "📋 3. Output JSON"])

# Graph config for persistence
config = {"configurable": {"thread_id": st.session_state.session_id}}


def run_graph(inputs: Any, is_resume: bool = False):
    """Run or resume the LangGraph agent."""
    st.session_state.is_running = True
    
    try:
        if is_resume:
            logger.info("Resuming LangGraph agent after interrupt.")
            # We are responding to an interrupt
            result = st.session_state.graph.invoke(Command(resume=inputs), config=config)
        else:
            logger.info("Starting new LangGraph agent run.")
            # Initial run
            result = st.session_state.graph.invoke(inputs, config=config)

        # Check if the graph paused on an interrupt
        # LangGraph surfaces the interrupt payload in result["__interrupt__"]
        interrupts = result.get("__interrupt__", [])
        if interrupts:
            logger.info(f"Agent paused on interrupt: {interrupts[0].value.get('action')}")
            # We take the first interrupt payload
            st.session_state.current_interrupt = interrupts[0].value
            st.session_state.is_running = False
            return result # Returning the state snapshot
            
        else:
            logger.info("Agent run completed successfully without interrupts.")
            st.session_state.current_interrupt = None
            st.session_state.is_running = False
            return result

    except Exception as e:
        error_msg = str(e)
        if "timeout" in error_msg.lower():
            logger.error(f"Graph execution timeout: {error_msg}")
            st.error("LLM Request Timeout: The provider took too long to respond. Please try again.")
            st.toast("LLM Timeout!", icon="⏳")
        else:
            logger.exception(f"Graph execution failed: {error_msg}")
            st.error(f"Graph execution failed: {error_msg}")
            st.toast("Execution error!", icon="❌")
            
        st.session_state.is_running = False
        return None

# ---------------------------------------------------------------------------
# Tab 1: Input & Upload
# ---------------------------------------------------------------------------
with tab1:
    st.markdown("### Upload Documentation")
    st.markdown(f"Supported formats: {get_supported_formats_display()}")
    
    uploaded_files = st.file_uploader(
        "Select files",
        accept_multiple_files=True,
        type=["csv", "xlsx", "xls", "md", "html", "htm", "pdf", "docx", "txt", "log", "json", "xml"],
    )

    st.markdown("### Additional Context (Optional)")
    user_context = st.text_area(
        "Provide any additional information about the portal or workflows that isn't in the docs.",
        height=100,
    )

    if st.button("🚀 Analyze & Generate Context", type="primary", disabled=st.session_state.is_running):
        if not uploaded_files:
            st.warning("Please upload at least one file.")
        else:
            with st.spinner("Parsing files..."):
                raw_files = []
                for f in uploaded_files:
                    raw_files.append((f.getvalue(), f.name))
                
                logger.info(f"Parsing {len(raw_files)} uploaded files.")
                parsed_docs = parse_multiple_files(raw_files)
                
                # Show parsing errors if any
                has_errors = False
                for d in parsed_docs:
                    if d.file_type == "unsupported":
                        logger.error(f"Failed to parse {d.filename}: {d.metadata.get('error')}")
                        st.error(f"Failed to parse {d.filename}: {d.metadata.get('error')}")
                        has_errors = True
                
                if not has_errors:
                    logger.info("All files parsed successfully.")
                    st.success(f"Successfully parsed {len(parsed_docs)} files.")
                    
                    # Add to chat history
                    st.session_state.messages.append({
                        "role": "user", 
                        "content": f"Uploaded {len(parsed_docs)} files. Context: {user_context}"
                    })
                    
                    # Prepare initial state
                    inputs = {
                        "documents": [
                            {"filename": d.filename, "content": d.content, "file_type": d.file_type}
                            for d in parsed_docs
                        ],
                        "user_inputs": [user_context] if user_context.strip() else [],
                        "phase": "started"
                    }
                    
                    with st.spinner("Agent is analyzing documents..."):
                        run_graph(inputs, is_resume=False)
                        st.rerun()

# ---------------------------------------------------------------------------
# Tab 2: Agent Chat (Questions)
# ---------------------------------------------------------------------------
with tab2:
    # Display chat history (simplified for UI)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # If we are paused waiting for user clarification
    if st.session_state.current_interrupt and st.session_state.current_interrupt.get("action") == "ask_user":
        interrupt_data = st.session_state.current_interrupt
        
        with st.chat_message("assistant"):
            st.markdown(interrupt_data["message"])
            st.markdown(interrupt_data["raw_text"])
            
        with st.form("clarification_form"):
            st.markdown("### Provide Clarifications")
            user_answer = st.text_area("Your answers:", height=150)
            submitted = st.form_submit_button("Submit Answers")
            
            if submitted:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": interrupt_data["raw_text"]
                })
                st.session_state.messages.append({
                    "role": "user",
                    "content": user_answer
                })
                
                logger.info("Submitting user clarification answers.")
                with st.spinner("Generating JSON..."):
                    resume_payload = {
                        "action": "answer",
                        "answers": [user_answer],
                        "raw_text": user_answer
                    }
                    run_graph(resume_payload, is_resume=True)
                    st.rerun()

# ---------------------------------------------------------------------------
# Tab 3: Output JSON (Review & Export)
# ---------------------------------------------------------------------------
with tab3:
    if st.session_state.current_interrupt and st.session_state.current_interrupt.get("action") == "review_json":
        st.success("JSON Generated Successfully!")
        
        interrupt_data = st.session_state.current_interrupt
        portal_context = interrupt_data.get("portal_context", {})
        workflows = interrupt_data.get("workflows", [])
        
        # Display as tabs
        wf_tabs = st.tabs(["🏢 Portal Info"] + [f"📋 Workflow: {wf.get('name', 'Unknown')}" for wf in workflows])
        
        with wf_tabs[0]:
            st.json(portal_context)
            
        for i, wf in enumerate(workflows):
            with wf_tabs[i+1]:
                st.json(wf)
                
        st.divider()
        st.markdown("### Review & Export")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Request Changes")
            with st.form("feedback_form"):
                feedback = st.text_area("What should be changed?", placeholder="E.g., The Submit Leave workflow is missing step 4 where the user clicks 'Confirm'.")
                submit_feedback = st.form_submit_button("Refine JSON")
                
                if submit_feedback and feedback:
                    logger.info("Submitting JSON refinement feedback.")
                    st.session_state.messages.append({
                        "role": "user",
                        "content": f"Requested JSON changes: {feedback}"
                    })
                    with st.spinner("Agent is refining JSON..."):
                        run_graph({
                            "action": "refine",
                            "feedback": feedback
                        }, is_resume=True)
                        st.rerun()
                        
        with col2:
            st.markdown("#### Approve")
            st.markdown("If the JSON looks correct, approve it to finish the process and download the files.")
            
            # Prepare files for export
            wf_files = []
            for wf in workflows:
                safe_name = sanitize_filename(wf.get("name", "workflow"))
                wf_id = wf.get("id", f"wf_{len(wf_files)}")
                filename = f"{wf_id}_{safe_name}.json"
                # Wrap in {"workflow": {...}} as per schema
                wf_files.append((filename, {"workflow": wf}))
                
            zip_bytes = create_zip_export(portal_context, wf_files)
            
            st.download_button(
                label="📦 Download ZIP Export",
                data=zip_bytes,
                file_name=f"portal_context_{sanitize_filename(portal_context.get('portal', {}).get('name', 'export'))}.zip",
                mime="application/zip",
                type="primary",
            )
            
            if st.button("✅ Finish Session"):
                logger.info("User approved JSON and finished session.")
                run_graph({"action": "approve"}, is_resume=True)
                st.success("Session completed! You can start a new session from the sidebar.")
                st.balloons()
    else:
        st.info("No JSON generated yet. Complete the steps in the previous tabs.")
