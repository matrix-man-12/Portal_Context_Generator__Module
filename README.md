# Portal Context Generator Module

The **Portal Context Generator** is an advanced Python-based utility module built to automate the extraction of UI workflows, portal structures, and platform behaviors from raw, unstructured documentation. 

It is designed to ingest human-readable documentation (like PDFs, Word Docs, and CSVs) and, using a Human-in-the-Loop AI Agent, produce a highly structured, machine-readable JSON output describing exactly how to navigate and automate tasks on a given web portal.

## Features

- **Multi-Format Ingestion**: Upload `.csv`, `.xlsx`, `.md`, `.html`, `.pdf`, and `.docx` files simultaneously.
- **Stateful AI Agent (LangGraph)**: The agent analyzes your documents and pauses execution to ask you clarifying questions when ambiguities arise.
- **Iterative Refinement**: Review the generated JSON within the UI and request modifications until it is perfectly aligned with your expectations.
- **Strict Output Schema**: Uses Pydantic to ensure all outputs are strictly formatted for downstream automation bots.
- **Flexible LLM Support**: Choose between Google Gemini, Anthropic Claude, or use your own local OpenAI-compatible models (like LM Studio or Ollama) for completely private execution.

---

## Installation

### 1. Requirements
Ensure you have Python 3.9+ installed on your system.

### 2. Setup Virtual Environment
Clone the repository and set up a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows**: `.\\venv\\Scripts\\activate`
- **Mac/Linux**: `source venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Copy the `.env.example` file to a `.env` file in the root directory:
```bash
cp .env.example .env
```
Fill in your `GOOGLE_API_KEY` and `ANTHROPIC_API_KEY` if you plan to use those cloud providers.

---

## Usage

Start the Streamlit application:
```bash
streamlit run app.py
```

### Typical Workflow:
1. **Configure Provider**: Open the sidebar, select your preferred LLM provider, enter your API key or Local Base URL, and click **Connect**.
2. **Upload Docs**: On the **Input & Upload** tab, drop your portal documentation files and add any manual context. Click Generate.
3. **Answer Questions**: The agent will transition to the **Agent Chat** tab. It will read the documents and ask you questions if anything is missing. Provide your answers to continue.
4. **Review JSON**: Once generated, switch to the **Output JSON** tab. Review the specific workflows. You can request changes iteratively.
5. **Export**: Click **Approve & Export** to download a ZIP file containing the split JSON configurations.

---

## Documentation

Extensive, component-level documentation can be found in the `docs/` folder. 
For an interactive reading experience, open `docs/HTML_docs/01_architecture_overview.html` in your browser.

- `01_architecture_overview.md` - Core system design
- `02_llm_configuration.md` - Supported models and factories
- `03_document_parsing.md` - Ingestion and truncation logic
- `04_agent_workflow.md` - LangGraph state machine details
- `05_output_and_schemas.md` - Pydantic structures
- `06_logging_and_debugging.md` - Trace and file logging
