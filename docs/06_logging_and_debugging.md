# Logging and Debugging

The application implements a robust logging system to aid in debugging, monitoring agent behavior, and tracking execution flows without cluttering the Streamlit UI.

## The Logger Utility (`utils/logger.py`)

The application uses Python's built-in `logging` module, wrapped in a utility function `setup_logger(name)`. 

### Dual Logging System
Every logger initialized in the codebase outputs to two destinations simultaneously:

1. **Terminal Console (`StreamHandler`)**:
   - **Level**: `INFO` and above.
   - **Format**: `[LEVEL] logger_name: Message`
   - **Purpose**: Provides short, meaningful, and immediate feedback to the developer running the Streamlit app locally. It traces major events like LLM connections, graph execution steps, and interruptions.

2. **File Log (`RotatingFileHandler`)**:
   - **Level**: `DEBUG` and above.
   - **Format**: `Timestamp | logger_name (fixed width) | LEVEL | Message`
   - **Location**: `logs/app.log` (The `logs` directory is automatically created).
   - **Rotation**: The file rolls over at 5MB, keeping up to 3 backup files to prevent disk exhaustion.
   - **Purpose**: Provides deep, detailed tracing. This is where you look when you need to see exactly why a parser failed or why the LangGraph state machine errored out.

## Key Log Points
- **`app.py`**: User actions, session resets, LLM connections, graph initializations, and interrupts.
- **`parsers/file_parser.py`**: Which files are processed, character counts, and specific exceptions (e.g., corrupted PDFs).
- **`agent/nodes/*.py`**: Every LangGraph node logs when it starts an LLM invocation, when it completes, how many characters it generated, and logs full stack traces (`logger.exception()`) if the LLM call fails.
