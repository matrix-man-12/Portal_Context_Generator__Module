# Document Parsing Pipeline

Because documentation can come in a wide variety of formats, the system uses a unified file parsing pipeline (`parsers/file_parser.py`) to extract clean text for the LLM.

## Supported Formats
- **CSV & Excel (.csv, .xlsx, .xls)**: Parsed using `pandas`. Output is formatted as a Markdown table.
- **Word (.docx)**: Parsed using `python-docx`. Extracts headings, paragraphs, and tables.
- **PDF (.pdf)**: Parsed using `PyPDF2`. Extracts raw text page by page.
- **HTML/XML (.html, .xml)**: Parsed using `BeautifulSoup4`. Strips scripts, styles, and structural tags, keeping only the human-readable text.
- **Markdown & Plaintext (.md, .txt, .log, .json)**: Read directly as UTF-8 strings.

## The Parsing Process
When a user uploads files through Streamlit, the `parse_multiple_files()` function processes them:
1. It identifies the file type by extension.
2. It routes the byte stream to the specific parsing function.
3. It returns a list of `ParsedDocument` dataclasses containing the filename, type, character count, and raw text.

## Truncation and Context Limits
Large files, especially CSVs or Excels, can quickly exceed the context window limits of an LLM.
- **Table Limits**: Excel and CSV files are limited to a preview of their first 100 rows if they exceed 500 rows.
- **Global Truncation**: When the `document_processor` node consolidates all the text, it enforces a hard cap of `200,000` characters. If the total combined text is larger, it cuts the document short and appends a `[TRUNCATED]` warning to prevent LLM payload rejection.
