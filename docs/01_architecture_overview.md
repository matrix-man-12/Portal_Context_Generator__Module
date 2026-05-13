# Architecture Overview

## Purpose
The **Portal Context Generator** is a specialized utility module designed to automate the extraction of UI workflows, portal structures, and platform behaviors from raw, unstructured documentation. 

The primary goal of this tool is to provide a comprehensive, automation-ready JSON output that downstream systems (like headless browsers and DOM automation tools) can ingest to understand the environment they are operating in.

## High-Level Architecture

The project is built on three core pillars:
1. **User Interface (Streamlit)**: A web-based frontend that allows users to upload documents, configure their LLM provider, interact with the agent for clarifying questions, and download the final ZIP output.
2. **Stateful Agent (LangGraph)**: An event-driven, human-in-the-loop state machine. It orchestrates the flow of data from raw text to structured JSON, pausing execution when it needs user input.
3. **Structured Enforcer (Pydantic + LangChain)**: Strict schema definitions that force the underlying LLM to return data exactly as required by the automation scripts.

## Data Flow
1. **Ingestion**: User uploads multiple files (PDFs, Word docs, CSVs, etc.) via the UI.
2. **Parsing**: The unified parser normalizes all documents into plain text.
3. **Analysis**: The LangGraph agent analyzes the text and builds a conceptual understanding of the portal.
4. **Clarification**: If ambiguities exist, the graph interrupts and asks the user questions.
5. **Generation**: The agent generates a structured JSON payload conforming to the Pydantic schemas.
6. **Refinement**: The user reviews the JSON in the UI and can request changes. The agent updates the JSON iteratively until approved.
7. **Export**: The approved JSON is exported as a ZIP file containing the overall portal info and individual workflow JSON files.
