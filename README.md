# Portal Context Generator Module

A Streamlit and LangGraph-powered AI tool to generate structured portal workflows from raw documentation.

This module ingests portal documentation (CSV, Excel, Markdown, HTML, PDF, DOCX) and uses a human-in-the-loop iterative agent to produce well-structured, automation-ready JSON describing portal UI interactions.

## Features

- **Multi-Format Parsing**: Extracts text from PDFs, Word docs, Excel sheets, HTML, and more.
- **LLM Agnostic**: Supports Google Gemini, Anthropic Claude, and any local/OpenAI-compatible LLM (e.g., LM Studio, Ollama).
- **Human-in-the-Loop Agent**: Uses LangGraph's `interrupt()` to ask clarifying questions when documents are ambiguous.
- **Structured JSON Output**: Uses Pydantic and `.with_structured_output()` to guarantee adherence to a predefined schema.
- **Iterative Refinement**: Allows users to request specific changes to the generated JSON before final export.
- **Split File Export**: Generates one JSON file per workflow and packages them into a convenient ZIP download.

## Setup

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Copy `.env.example` to `.env` and add your API keys:
   ```bash
   cp .env.example .env
   ```
   *(Alternatively, you can enter API keys directly in the app's sidebar during runtime).*

## Running the Application

Start the Streamlit server:
```bash
streamlit run app.py
```

## Usage Workflow

1. **Configure LLM**: In the sidebar, select your provider (Gemini, Claude, or Local), enter your API key (and Base URL if local), and click "Connect & Initialize".
2. **Upload Docs**: On Tab 1, upload your portal documentation and provide any extra context. Click "Analyze & Generate".
3. **Answer Questions**: On Tab 2, the agent will ask clarifying questions if it finds gaps in the documentation. Provide your answers to continue.
4. **Review & Refine**: On Tab 3, review the generated JSON. If something is missing, type your feedback and click "Refine JSON".
5. **Export**: Once satisfied, click "Finish Session" and download the ZIP file containing all workflow JSONs.
