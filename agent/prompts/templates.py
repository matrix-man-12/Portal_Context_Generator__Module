"""
LLM prompt templates for the Portal Context Generator agent.

Each prompt is designed for a specific node in the LangGraph workflow.
Prompts use f-string placeholders for dynamic content injection.
"""

# ---------------------------------------------------------------------------
# System prompt — defines the agent's persona
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a Portal Context Analyst — an expert at understanding internal web portals \
and documenting their workflows in structured formats.

Your job is to analyze documentation, screenshots, and user descriptions of internal portals, \
then produce precise, actionable JSON descriptions of:
- What the portal is and does
- The step-by-step UI workflows users perform on it
- Each individual UI action (click, type, select, navigate, etc.)

IMPORTANT RULES:
1. You describe HIGH-LEVEL UI actions (what a human sees and does), NOT DOM selectors or code.
2. Steps should read like instructions: "Click the Submit button", "Select 'Casual Leave' from the dropdown".
3. Be specific about target elements — use the exact label/text visible on the UI.
4. Include expected results for each step — what happens after the action.
5. If information is ambiguous or missing, ask clarifying questions rather than guessing.
6. Use the exact action types and target types from the schema — don't invent new ones.

Action types: click, input_text, input_date, select_dropdown, toggle, upload_file, scroll, hover, navigate, wait, verify
Target types: button, link, menu_item, dropdown, text_input, text_area, date_picker, checkbox, radio_button, \
toggle_switch, file_input, tab, modal, page, section, table_row, icon, other
"""

# ---------------------------------------------------------------------------
# Document analysis prompt
# ---------------------------------------------------------------------------

DOCUMENT_ANALYSIS_PROMPT = """Analyze the following documents about a portal/application and extract:

1. **Portal Identity**: Name, purpose, URL (if mentioned), category
2. **Navigation Structure**: Main menu items, tabs, sidebar entries
3. **Available Workflows/Tasks**: List every distinct task or workflow a user can perform
4. **UI Elements**: Common buttons, forms, tables, modals mentioned
5. **User Roles**: Any different user roles or permissions mentioned

Documents:
{documents}

{user_context}

Provide a comprehensive analysis. Be thorough — every workflow and UI element matters. \
If something is unclear or could be interpreted multiple ways, note it as a question to ask the user later."""

# ---------------------------------------------------------------------------
# Question generation prompt
# ---------------------------------------------------------------------------

QUESTION_GENERATION_PROMPT = """Based on your analysis of the portal documentation, you've identified the following:

**Portal Analysis:**
{analysis}

**Source Documents:**
{document_names}

Now, identify any GAPS or AMBIGUITIES in the documentation. Generate targeted questions that will help \
produce accurate, complete workflow JSONs.

Focus on:
1. Missing steps in workflows (e.g., "The doc mentions submitting a form but doesn't list the fields")
2. Unclear navigation paths (e.g., "How do you get to the Settings page?")
3. Missing workflows (e.g., "The doc mentions a 'Reports' section but doesn't describe what you do there")
4. UI element details (e.g., "Is the 'Status' field a dropdown or a text input?")
5. Preconditions and postconditions

Generate between 3 and 8 questions. Each question should be specific and actionable. \
Do NOT ask generic questions — only ask about things that are genuinely unclear from the documents.

If the documents are comprehensive and clear, you may generate fewer questions or state that \
no additional clarification is needed.

Format your response as a numbered list of questions."""

# ---------------------------------------------------------------------------
# JSON generation prompt
# ---------------------------------------------------------------------------

JSON_GENERATION_PROMPT = """Based on the portal analysis and user clarifications, generate the complete \
structured portal context.

**Portal Analysis:**
{analysis}

**User Clarifications:**
{clarifications}

**Source Documents:**
{document_names}

Generate the output in the EXACT schema format specified. You must produce:

1. **Portal Info**: name, description, url (if known), category
2. **UI Elements**: navigation items and common actions
3. **Workflows**: One complete workflow per task identified, with:
   - Unique ID (wf_001, wf_002, etc.)
   - Descriptive name
   - Clear description
   - Preconditions
   - Step-by-step actions (each with action type, target, target_type, description, expected_result)
   - Postconditions

CRITICAL RULES:
- Every step must have a valid action type from: click, input_text, input_date, select_dropdown, \
toggle, upload_file, scroll, hover, navigate, wait, verify
- Every step must have a valid target_type from: button, link, menu_item, dropdown, text_input, \
text_area, date_picker, checkbox, radio_button, toggle_switch, file_input, tab, modal, page, section, \
table_row, icon, other
- Step numbers must be sequential starting from 1
- Be specific about UI element names — use the exact labels visible on the portal
- Include ALL workflows identified in the analysis, don't skip any"""

# ---------------------------------------------------------------------------
# JSON refinement prompt
# ---------------------------------------------------------------------------

JSON_REFINEMENT_PROMPT = """The user has reviewed the generated portal context JSON and has feedback.

**Current JSON:**
{current_json}

**User Feedback:**
{feedback}

Apply the user's requested changes to the JSON. Maintain the exact same schema structure. \
Only modify what the user specifically asked to change — keep everything else identical.

If the user's feedback is unclear, ask a clarifying question. Otherwise, produce the updated JSON."""
