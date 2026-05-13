# Output and Schemas

To ensure that downstream automation scripts (like UI automation bots) receive predictable and strongly typed data, the Portal Context Generator strictly enforces output formats using Pydantic schemas.

## Schemas (`schemas/portal_schema.py`)

We define three primary Pydantic `BaseModel` classes:
1. **`PortalContext`**: Describes the global properties of the platform.
   - `id`, `name`, `url` (optional), `description`, `environment_type`.
   - `global_navigation`: A list of dictionaries describing main navigation elements.
   - `user_roles`: The types of users that interact with the portal.
2. **`Workflow`**: Describes an individual, distinct task.
   - `id`, `name`, `description`, `trigger`, `expected_outcome`.
   - `steps`: An ordered list of steps to complete the workflow.
     - Each step contains `step_number`, `action`, `element_type`, `element_identifier`, `input_value`, and `notes`.
3. **`GeneratedOutput`**: A wrapper schema holding one `PortalContext` and a list of `Workflow` objects. This is what the LLM is instructed to generate.

## Enforcement Mechanism
We use LangChain's `.with_structured_output(GeneratedOutput)` method inside the `json_generator` node. This forces the LLM to output valid JSON that matches the exact keys, types, and nested arrays defined in the Pydantic classes.

## Export Format
When the user clicks "Download ZIP Export", the Streamlit app generates an archive containing:
- `_portal_info.json`: Contains the `PortalContext` data.
- `<workflow_id>_<workflow_name>.json`: One JSON file for each workflow identified, containing the steps to execute that specific task.

This segmented approach allows automation systems to load generic portal metadata once, and then load specific workflow JSONs only when those tasks need to be executed.
