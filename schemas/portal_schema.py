"""
Pydantic models defining the structured JSON output schema for portal context.

These models serve two purposes:
1. Validate LLM-generated JSON output
2. Enable LangChain's `.with_structured_output()` for reliable schema adherence

Output is split into separate files:
- _portal_info.json: Portal metadata + UI elements
- wf_XXX_<name>.json: One file per workflow
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ActionType(str, Enum):
    """High-level UI action types (NOT DOM-level)."""
    CLICK = "click"
    INPUT_TEXT = "input_text"
    INPUT_DATE = "input_date"
    SELECT_DROPDOWN = "select_dropdown"
    TOGGLE = "toggle"
    UPLOAD_FILE = "upload_file"
    SCROLL = "scroll"
    HOVER = "hover"
    NAVIGATE = "navigate"
    WAIT = "wait"
    VERIFY = "verify"


class TargetType(str, Enum):
    """Types of UI elements that actions target."""
    BUTTON = "button"
    LINK = "link"
    MENU_ITEM = "menu_item"
    DROPDOWN = "dropdown"
    TEXT_INPUT = "text_input"
    TEXT_AREA = "text_area"
    DATE_PICKER = "date_picker"
    CHECKBOX = "checkbox"
    RADIO_BUTTON = "radio_button"
    TOGGLE_SWITCH = "toggle_switch"
    FILE_INPUT = "file_input"
    TAB = "tab"
    MODAL = "modal"
    PAGE = "page"
    SECTION = "section"
    TABLE_ROW = "table_row"
    ICON = "icon"
    OTHER = "other"


class WorkflowStep(BaseModel):
    """A single step in a workflow — describes one high-level UI action."""
    step_number: int = Field(..., description="Sequential step number starting from 1")
    action: ActionType = Field(..., description="The type of UI action to perform")
    target: str = Field(..., description="Human-readable description of the UI element to interact with")
    target_type: TargetType = Field(..., description="The type of UI element being targeted")
    description: str = Field(..., description="Detailed description of what this step does and why")
    expected_result: str = Field(..., description="What should happen after this step is completed")
    options: Optional[list[str]] = Field(None, description="Available options (for dropdowns, radio buttons, etc.)")
    notes: Optional[str] = Field(None, description="Additional context or edge cases for this step")


class Workflow(BaseModel):
    """A complete workflow/task with ordered steps."""
    id: str = Field(..., description="Unique workflow identifier, e.g., 'wf_001'")
    name: str = Field(..., description="Human-readable workflow name")
    description: str = Field(..., description="What this workflow accomplishes end-to-end")
    preconditions: list[str] = Field(
        default_factory=list,
        description="Conditions that must be true before starting this workflow"
    )
    steps: list[WorkflowStep] = Field(..., description="Ordered list of steps to complete this workflow")
    postconditions: list[str] = Field(
        default_factory=list,
        description="Expected state after workflow completion"
    )
    notes: Optional[str] = Field(None, description="Additional context, edge cases, or confidence notes")


class PortalInfo(BaseModel):
    """Top-level portal metadata."""
    name: str = Field(..., description="Name of the portal")
    description: str = Field(..., description="What this portal is and what it does")
    url: Optional[str] = Field(None, description="Portal URL if known")
    category: Optional[str] = Field(None, description="Portal category (e.g., HR, Finance, IT)")


class UIElements(BaseModel):
    """Common UI elements and navigation structure of the portal."""
    navigation: list[str] = Field(
        default_factory=list,
        description="Main navigation items/menu entries"
    )
    common_actions: list[str] = Field(
        default_factory=list,
        description="Commonly available actions across the portal (e.g., Login, Search)"
    )


class PortalMetadata(BaseModel):
    """Metadata about the generation process."""
    generated_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="ISO timestamp of when this was generated"
    )
    source_documents: list[str] = Field(
        default_factory=list,
        description="List of source document filenames used"
    )
    version: str = Field(default="1.0", description="Schema version")
    total_workflows: int = Field(default=0, description="Total number of workflows generated")
    confidence_notes: Optional[str] = Field(
        None,
        description="Notes about inference confidence, gaps, or assumptions"
    )


class PortalContext(BaseModel):
    """
    Top-level portal context — written to _portal_info.json.
    Contains portal metadata, UI elements, and generation metadata.
    Workflows are stored separately (one file each).
    """
    portal: PortalInfo
    ui_elements: UIElements = Field(default_factory=UIElements)
    metadata: PortalMetadata = Field(default_factory=PortalMetadata)


class WorkflowFile(BaseModel):
    """Wrapper for a single workflow file output."""
    workflow: Workflow


class GeneratedOutput(BaseModel):
    """
    Complete generated output — not written to a single file,
    but used internally to hold all generated data before splitting into files.
    """
    portal_context: PortalContext
    workflows: list[Workflow] = Field(default_factory=list)

    def get_portal_info_dict(self) -> dict:
        """Get the portal info JSON (for _portal_info.json)."""
        ctx = self.portal_context.model_copy()
        ctx.metadata.total_workflows = len(self.workflows)
        return ctx.model_dump(mode="json")

    def get_workflow_dicts(self) -> list[tuple[str, dict]]:
        """
        Get list of (filename, workflow_dict) tuples.
        Filename format: wf_XXX_<sanitized_name>.json
        """
        results = []
        for wf in self.workflows:
            # Sanitize workflow name for filename
            safe_name = wf.name.lower().replace(" ", "_")
            safe_name = "".join(c for c in safe_name if c.isalnum() or c == "_")
            filename = f"{wf.id}_{safe_name}.json"
            results.append((filename, WorkflowFile(workflow=wf).model_dump(mode="json")))
        return results
