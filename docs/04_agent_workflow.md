# Agent Workflow (LangGraph)

The core logic of the application is powered by a stateful **LangGraph** agent. It operates as a continuous pipeline that can pause, wait for user input, and resume exactly where it left off.

## Agent State
The graph state is defined in `agent/state.py` as a `TypedDict`. It holds:
- The parsed `documents` and `user_inputs`.
- The intermediary `analysis` and generated `questions`.
- The user's `answers` to those questions.
- The final `portal_context` and `workflows` JSON objects.

## Nodes and Flow

1. **`document_processor`**:
   Takes the array of `ParsedDocument` objects and consolidates them into a single string formatted with clear headers. No LLM call is made here.

2. **`context_builder`**:
   The first heavy LLM call. It reads the consolidated document text and generates a comprehensive, plain-text analysis of what the portal does and what workflows it contains.

3. **`question_generator`**:
   Analyzes the context built in the previous step to identify missing data, ambiguities, or gaps. 
   - **Interrupt Mechanism**: If questions are generated, the graph calls `interrupt()`. Execution halts immediately. The Streamlit UI detects this interrupt and presents the questions to the user. When the user submits their answers, the graph resumes via `Command(resume=answers)`.

4. **`json_generator`**:
   Uses the LLM configured with `.with_structured_output()` to force the generation of strict JSON based on the Pydantic schemas, utilizing both the initial analysis and the user's answers.

5. **`json_refiner`**:
   Presents the generated JSON back to the user via another `interrupt()`. 
   - If the user approves, the graph terminates (`END`). 
   - If the user requests changes (provides feedback), the LLM takes the feedback and the current JSON, modifies the JSON, and loops back to the review interrupt.

## Persistence
To maintain the chat session across Streamlit reruns, the graph uses `SqliteSaver` (from `langgraph.checkpoint.sqlite`). All graph states are saved to a local `sessions.db` file. Every execution runs within a specific `thread_id` tied to the user's Streamlit session ID.
