# Portal Context Generator Module — Task List

> **Last Updated**: 2026-05-13  
> **Legend**: `[ ]` Todo | `[/]` In Progress | `[x]` Done

---

## Phase 0: Project Setup
- [x] Create Python virtual environment (`venv`)
- [x] Create `requirements.txt` with all dependencies
- [x] Install dependencies in venv
- [x] Create `.env.example` with API key placeholders
- [x] Create project directory structure (all folders, `__init__.py` files)
- [x] Save finalized implementation plan to `docs/`
- [x] Save this task list to `docs/`

## Phase 1: Schema & Parsing Layer
- [x] Define Pydantic models in `schemas/portal_schema.py`
  - [x] `PortalInfo` model
  - [x] `WorkflowStep` model
  - [x] `Workflow` model  
  - [x] `UIElements` model
  - [x] `PortalContext` model (top-level)
  - [x] `GeneratedOutput` model (collection of workflow files)
- [x] Build file parser in `parsers/file_parser.py`
  - [x] CSV parsing (via pandas)
  - [x] Excel parsing (via pandas + openpyxl)
  - [x] Markdown parsing (direct read)
  - [x] HTML parsing (via BeautifulSoup)
  - [x] PDF parsing (via PyPDF2)
  - [x] Word/DOCX parsing (via python-docx)
  - [x] Plain text parsing
  - [x] Unified `parse_file()` function with file type detection
  - [x] `ParsedDocument` dataclass for output
- [ ] Test parsing with sample files of each type

## Phase 2: LLM Provider Configuration
- [x] Create LLM provider factory in `utils/helpers.py`
  - [x] Gemini provider setup (`langchain-google-genai`)
  - [x] Anthropic Claude provider setup (`langchain-anthropic`)
  - [x] Local/OpenAI-compatible provider setup (`langchain-openai` with `base_url`)
  - [x] Provider validation (test connection before starting agent)
- [ ] Test each provider individually

## Phase 3: Agent Prompts
- [x] Write prompt templates in `agent/prompts/templates.py`
  - [x] `DOCUMENT_ANALYSIS_PROMPT` — Extract portal info from documents
  - [x] `QUESTION_GENERATION_PROMPT` — Identify gaps, generate questions
  - [x] `JSON_GENERATION_PROMPT` — Produce structured workflow JSON
  - [x] `JSON_REFINEMENT_PROMPT` — Modify JSON based on user feedback
  - [x] `SYSTEM_PROMPT` — Overall agent persona and behavior

## Phase 4: Agent Nodes
- [x] Define agent state in `agent/state.py`
- [x] Build `document_processor.py` node
  - [x] Consolidate parsed documents into LLM-ready format
  - [x] Truncate/chunk if documents exceed context window
- [x] Build `context_builder.py` node
  - [x] Extract portal metadata (name, URL, category)
  - [x] Identify workflow list from documents
- [x] Build `question_generator.py` node
  - [x] Identify ambiguities and gaps
  - [x] Generate targeted clarifying questions
  - [x] Use `interrupt()` to pause for user input
- [x] Build `json_generator.py` node
  - [x] Generate portal info JSON
  - [x] Generate individual workflow JSONs
  - [x] Validate against Pydantic schema
- [x] Build `json_refiner.py` node
  - [x] Parse user change requests
  - [x] Apply modifications to existing JSON
  - [x] Use `interrupt()` to present updated JSON for review

## Phase 5: LangGraph Workflow
- [x] Wire up the graph in `agent/graph.py`
  - [x] Define node connections and edges
  - [x] Implement conditional routing (approve vs. refine)
  - [x] Add SQLite checkpointer for state persistence
  - [x] Compile the graph
- [ ] Test full agent flow with mock inputs

## Phase 6: Streamlit UI
- [x] Build `app.py` — main application
  - [x] Sidebar: LLM provider selection
    - [x] Provider dropdown (Gemini / Claude / Local)
    - [x] API key input (password masked)
    - [x] Base URL input (for local LLMs, conditional)
    - [x] Model name input (for local LLMs, conditional)
    - [x] Connection test button
  - [x] Tab 1: Input & Upload
    - [x] Multi-file uploader with supported format list
    - [x] Uploaded file list display with badges
    - [x] Free-text input area for additional context
    - [x] "Generate Portal Context" button
  - [x] Tab 2: Agent Chat
    - [x] Chat message display (agent questions, user answers)
    - [x] Phase/progress indicator
    - [x] User input for answering questions
    - [x] "Continue" button to resume agent after input
  - [x] Tab 3: Output JSON
    - [x] Workflow file tabs
    - [x] JSON pretty-print display
    - [x] "Request Changes" feedback input + button
    - [x] "Approve & Export" button
    - [x] ZIP download for all files
    - [x] Individual JSON file download buttons
- [x] Session state management (persist across reruns)
- [x] Error handling and user feedback (toast notifications)

## Phase 7: Integration & Testing
- [-] (Skipped) End-to-end test: upload real docs → generate JSON → export
- [-] (Skipped) Test with Gemini provider
- [-] (Skipped) Test with Claude provider
- [-] (Skipped) Test with local LLM provider
- [-] (Skipped) Test iterative refinement (multiple rounds of feedback)
- [-] (Skipped) Test file parsing edge cases (large files, empty files, mixed formats)
- [-] (Skipped) Test session resume (close and reopen)

## Phase 8: Polish & Documentation
- [x] Add loading spinners and progress messages
- [x] Add error handling for LLM failures / timeouts
- [x] Write README.md with setup and usage instructions
- [x] Update this task list with final status
