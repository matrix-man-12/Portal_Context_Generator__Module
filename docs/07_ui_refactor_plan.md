# UI Refactoring: Consolidated Chat and Output Views

The current layout uses 3 separate tabs (Input, Chat, and Output), which fragments the user experience. We will streamline this into a two-view architecture, creating a much more cohesive "chat with my documents" flow.

## Proposed Changes

### 1. Tab Consolidation
- Replace the 3 tabs (`tab1`, `tab2`, `tab3`) with 2 tabs: `💬 Chat Interface` and `📋 Generated Output`.
- The first tab will handle **both** document ingestion and conversational clarification.

### 2. Unified Input Mechanism
- Remove the `st.file_uploader` and the dedicated "Generate Portal Context" button.
- Utilize Streamlit 1.40+'s upgraded `st.chat_input` widget configured with `accept_file="multiple"`.
- This allows users to drop PDFs, Word Docs, or CSVs directly into the chat input box along with any contextual text messages, exactly like popular LLM interfaces.

### 3. Dynamic State Routing
- When the user submits the `st.chat_input`:
  - **If no session is running**: We treat any attached files as the initial portal documentation. The system parses them, appends the user's text as context, and kicks off the LangGraph agent.
  - **If the agent is paused on an interrupt (`ask_user`)**: We treat the text as the answer to the clarifying questions.
  - **If the agent is paused on `review_json`**: We treat the text as the "Request Changes" feedback, triggering the `json_refiner` node.

### 4. Streamlined Output View
- The `📋 Generated Output` tab will only be populated when the JSON is successfully generated.
- It will contain the workflow tabs, the actual JSON data, and the buttons to **Approve & Export** the ZIP file.
