import os

# Create directory if not exists
os.makedirs("docs/HTML_docs", exist_ok=True)

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portal Context Generator Docs</title>
    <style>
        :root {
            --bg-main: #faf9f6;
            --bg-sidebar: #f0f4f8;
            --text-main: #333333;
            --text-muted: #555555;
            --border-color: #e2e8f0;
            --accent-bg: #e0f2fe;
            --accent-border: #bae6fd;
            --code-bg: #f1f5f9;
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: system-ui, -apple-system, sans-serif;
            background: var(--bg-main);
            color: var(--text-main);
            display: flex;
            line-height: 1.6;
        }

        /* Sidebar Navigation */
        .sidebar {
            width: 250px;
            background: var(--bg-sidebar);
            border-right: 1px solid var(--border-color);
            padding: 2rem 1.5rem;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
        }

        .sidebar h2 {
            font-size: 1.2rem;
            margin-bottom: 1.5rem;
            color: #1e293b;
            font-weight: 600;
        }

        .nav-links { list-style: none; }
        .nav-links li { margin-bottom: 0.25rem; }
        .nav-links a {
            text-decoration: none;
            color: var(--text-muted);
            padding: 0.5rem;
            display: block;
            border-radius: 4px;
            font-size: 0.95rem;
        }

        .nav-links a:hover, .nav-links a.active {
            background: var(--border-color);
            color: #0f172a;
            font-weight: 600;
        }

        /* Main Content */
        .main-content {
            margin-left: 250px;
            padding: 3rem 4rem;
            max-width: 900px;
            width: 100%;
        }

        h1 { font-size: 2.2rem; margin-bottom: 1.5rem; color: #1e293b; }
        h2 { font-size: 1.5rem; margin: 2rem 0 1rem; color: #334155; border-bottom: 1px solid var(--border-color); padding-bottom: 0.3rem;}
        h3 { font-size: 1.2rem; margin: 1.5rem 0 0.5rem; color: #475569; }
        p { margin-bottom: 1rem; }
        
        /* Cards */
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }

        .card {
            background: #ffffff;
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 1.2rem;
        }

        .card h3 { margin-top: 0; color: #334155; }
        .card p { margin-bottom: 0; font-size: 0.95rem; }

        /* Lists */
        .styled-list {
            margin-left: 1.5rem;
            margin-bottom: 1.5rem;
        }
        .styled-list li {
            margin-bottom: 0.5rem;
        }

        /* Code Blocks */
        pre {
            background: var(--code-bg);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 1rem;
            overflow-x: auto;
            margin-bottom: 1rem;
        }

        code {
            font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
            font-size: 0.9rem;
            color: #0f172a;
        }

        p code, li code {
            background: var(--code-bg);
            padding: 0.1rem 0.3rem;
            border-radius: 3px;
        }

        /* Callouts */
        .callout {
            background: var(--accent-bg);
            border-left: 4px solid var(--accent-border);
            padding: 1rem 1.5rem;
            border-radius: 0 4px 4px 0;
            margin: 1.5rem 0;
        }
        .callout p { margin-bottom: 0; color: #0f172a; }

    </style>
</head>
<body>
    <nav class="sidebar">
        <h2>Portal Context</h2>
        <ul class="nav-links">
            <li><a href="01_architecture_overview.html" class="{active_1}">1. Architecture</a></li>
            <li><a href="02_llm_configuration.html" class="{active_2}">2. LLM Configuration</a></li>
            <li><a href="03_document_parsing.html" class="{active_3}">3. Document Parsing</a></li>
            <li><a href="04_agent_workflow.html" class="{active_4}">4. Agent Workflow</a></li>
            <li><a href="05_output_and_schemas.html" class="{active_5}">5. Output Schemas</a></li>
            <li><a href="06_logging_and_debugging.html" class="{active_6}">6. Logging</a></li>
            <li><a href="implementation_plan.html" class="{active_plan}">Implementation Plan</a></li>
            <li><a href="task_list.html" class="{active_task}">Task List</a></li>
        </ul>
    </nav>

    <main class="main-content">
        {content}
    </main>
</body>
</html>
"""

pages = [
    ("01_architecture_overview.html", "active_1", '''<h1 class="gradient-text">Architecture Overview</h1>
<h2>Purpose</h2>
<p>The <strong>Portal Context Generator</strong> is a specialized utility module designed to automate the extraction of UI workflows, portal structures, and platform behaviors from raw, unstructured documentation.</p>
<p>The primary goal of this tool is to provide a comprehensive, automation-ready JSON output that downstream systems (like headless browsers and DOM automation tools) can ingest to understand the environment they are operating in.</p>

<h2>High-Level Architecture</h2>
<p>The project is built on three core pillars:</p>
<div class="card-grid">
  <div class="card">
    <h3>1. User Interface (Streamlit)</h3>
    <p>A web-based frontend that allows users to upload documents, configure their LLM provider, interact with the agent for clarifying questions, and download the final ZIP output.</p>
  </div>
  <div class="card">
    <h3>2. Stateful Agent (LangGraph)</h3>
    <p>An event-driven, human-in-the-loop state machine. It orchestrates the flow of data from raw text to structured JSON, pausing execution when it needs user input.</p>
  </div>
  <div class="card">
    <h3>3. Structured Enforcer (Pydantic + LangChain)</h3>
    <p>Strict schema definitions that force the underlying LLM to return data exactly as required by the automation scripts.</p>
  </div>
</div>

<h2>Data Flow</h2>
<ol class="styled-list">
  <li><strong>Ingestion</strong>: User uploads multiple files (PDFs, Word docs, CSVs, etc.) via the UI.</li>
  <li><strong>Parsing</strong>: The unified parser normalizes all documents into plain text.</li>
  <li><strong>Analysis</strong>: The LangGraph agent analyzes the text and builds a conceptual understanding of the portal.</li>
  <li><strong>Clarification</strong>: If ambiguities exist, the graph interrupts and asks the user questions.</li>
  <li><strong>Generation</strong>: The agent generates a structured JSON payload conforming to the Pydantic schemas.</li>
  <li><strong>Refinement</strong>: The user reviews the JSON in the UI and can request changes. The agent updates the JSON iteratively until approved.</li>
  <li><strong>Export</strong>: The approved JSON is exported as a ZIP file containing the overall portal info and individual workflow JSON files.</li>
</ol>'''),

    ("02_llm_configuration.html", "active_2", '''<h1 class="gradient-text">LLM Configuration</h1>
<p>The Portal Context Generator supports multiple LLM providers, making it adaptable to different environments—from cloud-hosted models to completely air-gapped, local setups.</p>

<h2>Supported Providers</h2>
<p>We currently support three provider types:</p>
<div class="card-grid">
  <div class="card">
    <h3>1. Google Gemini</h3>
    <p>Default model: <code>gemini-2.5-flash</code></p>
  </div>
  <div class="card">
    <h3>2. Anthropic Claude</h3>
    <p>Default model: <code>claude-sonnet-4-20250514</code></p>
  </div>
  <div class="card">
    <h3>3. Local (OpenAI-compatible)</h3>
    <p>User-specified models via local endpoints.</p>
  </div>
</div>

<h2>Local LLMs (OpenAI Compatible)</h2>
<p>For local privacy and execution, the system can connect to local servers like <strong>LM Studio</strong> or <strong>Ollama</strong> that expose an OpenAI-compatible API endpoint.</p>
<ul class="styled-list">
  <li><strong>Base URL</strong>: e.g., <code>http://localhost:1234/v1</code> for LM Studio.</li>
  <li><strong>Model Name</strong>: The exact name of the model loaded in the local server (e.g., <code>meta-llama-3-8b-instruct</code>).</li>
  <li><strong>API Key</strong>: Usually left blank or as <code>"not-needed"</code>, depending on the server requirements.</li>
</ul>

<h2>How It Works</h2>
<p>The <code>create_llm</code> factory function initializes the appropriate LangChain <code>BaseChatModel</code>:</p>
<pre><code>def create_llm(provider, api_key, model_name=None, base_url=None, temperature=0.3):
    # Initializes ChatGoogleGenerativeAI, ChatAnthropic, or ChatOpenAI
    ...</code></pre>

<div class="callout">
  <p><strong>Temperature</strong>: Hardcoded to <code>0.3</code> across all providers. A lower temperature reduces hallucinations and ensures the LLM closely adheres to the structured JSON schemas.</p>
</div>

<h2>Connection Testing</h2>
<p>Before the LangGraph agent is initialized, the UI runs a connection test <code>test_llm_connection()</code>. It sends a simple <code>"Say 'OK' if you can hear me."</code> prompt to verify that API keys are valid and that local servers are running. If this fails, the user is presented with a clear error message in the UI and the agent is not started.</p>'''),

    ("03_document_parsing.html", "active_3", '''<h1 class="gradient-text">Document Parsing Pipeline</h1>
<p>Because documentation can come in a wide variety of formats, the system uses a unified file parsing pipeline (<code>parsers/file_parser.py</code>) to extract clean text for the LLM.</p>

<h2>Supported Formats</h2>
<ul class="styled-list">
  <li><strong>CSV & Excel (.csv, .xlsx, .xls)</strong>: Parsed using <code>pandas</code>. Output is formatted as a Markdown table.</li>
  <li><strong>Word (.docx)</strong>: Parsed using <code>python-docx</code>. Extracts headings, paragraphs, and tables.</li>
  <li><strong>PDF (.pdf)</strong>: Parsed using <code>PyPDF2</code>. Extracts raw text page by page.</li>
  <li><strong>HTML/XML (.html, .xml)</strong>: Parsed using <code>BeautifulSoup4</code>. Strips scripts, styles, and structural tags, keeping only the human-readable text.</li>
  <li><strong>Markdown & Plaintext (.md, .txt, .log, .json)</strong>: Read directly as UTF-8 strings.</li>
</ul>

<h2>The Parsing Process</h2>
<p>When a user uploads files through Streamlit, the <code>parse_multiple_files()</code> function processes them:</p>
<ol class="styled-list">
  <li>It identifies the file type by extension.</li>
  <li>It routes the byte stream to the specific parsing function.</li>
  <li>It returns a list of <code>ParsedDocument</code> dataclasses containing the filename, type, character count, and raw text.</li>
</ol>

<h2>Truncation and Context Limits</h2>
<p>Large files, especially CSVs or Excels, can quickly exceed the context window limits of an LLM.</p>
<div class="card-grid">
  <div class="card">
    <h3>Table Limits</h3>
    <p>Excel and CSV files are limited to a preview of their first 100 rows if they exceed 500 rows.</p>
  </div>
  <div class="card">
    <h3>Global Truncation</h3>
    <p>When the <code>document_processor</code> node consolidates all the text, it enforces a hard cap of <code>200,000</code> characters. If the total combined text is larger, it cuts the document short and appends a <code>[TRUNCATED]</code> warning to prevent LLM payload rejection.</p>
  </div>
</div>'''),

    ("04_agent_workflow.html", "active_4", '''<h1 class="gradient-text">Agent Workflow (LangGraph)</h1>
<p>The core logic of the application is powered by a stateful <strong>LangGraph</strong> agent. It operates as a continuous pipeline that can pause, wait for user input, and resume exactly where it left off.</p>

<h2>Agent State</h2>
<p>The graph state is defined in <code>agent/state.py</code> as a <code>TypedDict</code>. It holds:</p>
<ul class="styled-list">
  <li>The parsed <code>documents</code> and <code>user_inputs</code>.</li>
  <li>The intermediary <code>analysis</code> and generated <code>questions</code>.</li>
  <li>The user's <code>answers</code> to those questions.</li>
  <li>The final <code>portal_context</code> and <code>workflows</code> JSON objects.</li>
</ul>

<h2>Nodes and Flow</h2>
<div class="card-grid">
  <div class="card">
    <h3>1. document_processor</h3>
    <p>Takes the array of <code>ParsedDocument</code> objects and consolidates them into a single string formatted with clear headers. No LLM call is made here.</p>
  </div>
  <div class="card">
    <h3>2. context_builder</h3>
    <p>The first heavy LLM call. It reads the consolidated document text and generates a comprehensive, plain-text analysis of what the portal does and what workflows it contains.</p>
  </div>
  <div class="card">
    <h3>3. question_generator</h3>
    <p>Analyzes the context to identify gaps. If questions are generated, the graph calls <code>interrupt()</code>. Execution halts immediately and waits for user answers via the UI.</p>
  </div>
  <div class="card">
    <h3>4. json_generator</h3>
    <p>Uses the LLM configured with <code>.with_structured_output()</code> to force the generation of strict JSON based on the Pydantic schemas.</p>
  </div>
  <div class="card">
    <h3>5. json_refiner</h3>
    <p>Presents the generated JSON back to the user via another <code>interrupt()</code>. The user can approve to END the graph, or request changes which loops the graph back to refine the JSON.</p>
  </div>
</div>

<h2>Persistence</h2>
<div class="callout">
  <p>To maintain the chat session across Streamlit reruns, the graph uses <code>SqliteSaver</code> (from <code>langgraph.checkpoint.sqlite</code>). All graph states are saved to a local <code>sessions.db</code> file. Every execution runs within a specific <code>thread_id</code> tied to the user's Streamlit session ID.</p>
</div>'''),

    ("05_output_and_schemas.html", "active_5", '''<h1 class="gradient-text">Output and Schemas</h1>
<p>To ensure that downstream automation scripts (like UI automation bots) receive predictable and strongly typed data, the Portal Context Generator strictly enforces output formats using Pydantic schemas.</p>

<h2>Schemas (<code>schemas/portal_schema.py</code>)</h2>
<p>We define three primary Pydantic <code>BaseModel</code> classes:</p>

<div class="card-grid">
  <div class="card">
    <h3>1. PortalContext</h3>
    <p>Describes the global properties of the platform.</p>
    <ul class="styled-list" style="margin-top:0.5rem; margin-bottom:0;">
      <li><code>id</code>, <code>name</code>, <code>url</code>, <code>description</code></li>
      <li><code>global_navigation</code></li>
      <li><code>user_roles</code></li>
    </ul>
  </div>
  <div class="card">
    <h3>2. Workflow</h3>
    <p>Describes an individual, distinct task.</p>
    <ul class="styled-list" style="margin-top:0.5rem; margin-bottom:0;">
      <li><code>id</code>, <code>name</code>, <code>trigger</code></li>
      <li><code>steps</code>: ordered list of actions</li>
    </ul>
  </div>
  <div class="card">
    <h3>3. GeneratedOutput</h3>
    <p>A wrapper schema holding one <code>PortalContext</code> and a list of <code>Workflow</code> objects. This is what the LLM generates.</p>
  </div>
</div>

<h2>Enforcement Mechanism</h2>
<p>We use LangChain's <code>.with_structured_output(GeneratedOutput)</code> method inside the <code>json_generator</code> node. This forces the LLM to output valid JSON that matches the exact keys, types, and nested arrays defined in the Pydantic classes.</p>

<h2>Export Format</h2>
<div class="callout">
  <p>When the user clicks "Download ZIP Export", the Streamlit app generates an archive containing:</p>
  <ul class="styled-list" style="margin-top:1rem; margin-bottom:0;">
    <li><code>_portal_info.json</code>: Contains the <code>PortalContext</code> data.</li>
    <li><code>&lt;workflow_id&gt;_&lt;workflow_name&gt;.json</code>: One JSON file for each workflow identified, containing the steps to execute that specific task.</li>
  </ul>
</div>
<p>This segmented approach allows automation systems to load generic portal metadata once, and then load specific workflow JSONs only when those tasks need to be executed.</p>'''),

    ("06_logging_and_debugging.html", "active_6", '''<h1 class="gradient-text">Logging and Debugging</h1>
<p>The application implements a robust logging system to aid in debugging, monitoring agent behavior, and tracking execution flows without cluttering the Streamlit UI.</p>

<h2>The Logger Utility (<code>utils/logger.py</code>)</h2>
<p>The application uses Python's built-in <code>logging</code> module, wrapped in a utility function <code>setup_logger(name)</code>. </p>

<div class="card-grid">
  <div class="card">
    <h3>Terminal Console (StreamHandler)</h3>
    <p><strong>Level</strong>: <code>INFO</code> and above.</p>
    <p><strong>Format</strong>: <code>[LEVEL] logger_name: Message</code></p>
    <p><strong>Purpose</strong>: Provides short, meaningful, and immediate feedback to the developer running the Streamlit app locally.</p>
  </div>
  <div class="card">
    <h3>File Log (RotatingFileHandler)</h3>
    <p><strong>Level</strong>: <code>DEBUG</code> and above.</p>
    <p><strong>Location</strong>: <code>logs/app.log</code></p>
    <p><strong>Rotation</strong>: Rolls over at 5MB, keeping up to 3 backups.</p>
    <p><strong>Purpose</strong>: Provides deep, detailed tracing for pinpointing exactly why a parser or LLM call failed.</p>
  </div>
</div>

<h2>Key Log Points</h2>
<ul class="styled-list">
  <li><strong><code>app.py</code></strong>: User actions, session resets, LLM connections, graph initializations, and interrupts.</li>
  <li><strong><code>parsers/file_parser.py</code></strong>: Which files are processed, character counts, and specific exceptions (e.g., corrupted PDFs).</li>
  <li><strong><code>agent/nodes/*.py</code></strong>: Every LangGraph node logs when it starts an LLM invocation, when it completes, how many characters it generated, and logs full stack traces (<code>logger.exception()</code>) if the LLM call fails.</li>
</ul>''')
]

for filename, active_key, content in pages:
    page_html = TEMPLATE.replace("{content}", content)
    for i in range(1, 7):
        key = f"{{active_{i}}}"
        val = "active" if f"active_{i}" == active_key else ""
        page_html = page_html.replace(key, val)
    page_html = page_html.replace("{active_plan}", "")
    page_html = page_html.replace("{active_task}", "")
        
    with open(os.path.join("docs", "HTML_docs", filename), "w", encoding="utf-8") as f:
        f.write(page_html)

# Generate extra files
extra_files = [
    ("implementation_plan.md", "implementation_plan.html", "active_plan", "Implementation Plan"),
    ("task_list.md", "task_list.html", "active_task", "Task List")
]

for md_file, html_file, active_key, title in extra_files:
    md_path = os.path.join("docs", md_file)
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            md_content = f.read()
        
        # Simple HTML wrap for markdown content
        escaped_content = md_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        content_html = f"<h1>{title}</h1>\\n<pre style='white-space: pre-wrap; font-family: Consolas, monospace; font-size: 0.95rem; background: #fff; padding: 1.5rem; border: 1px solid var(--border-color); border-radius: 6px;'>{escaped_content}</pre>"
        
        page_html = TEMPLATE.replace("{content}", content_html)
        for i in range(1, 7):
            key = f"{{active_{i}}}"
            page_html = page_html.replace(key, "")
        page_html = page_html.replace("{active_plan}", "active" if active_key == "active_plan" else "")
        page_html = page_html.replace("{active_task}", "active" if active_key == "active_task" else "")
        
        with open(os.path.join("docs", "HTML_docs", html_file), "w", encoding="utf-8") as f:
            f.write(page_html)

print("Successfully generated 8 HTML docs.")
