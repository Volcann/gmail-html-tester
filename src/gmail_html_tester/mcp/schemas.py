from typing import Any
from pydantic import BaseModel, Field


class AnalyzeReq(BaseModel):
    tpl_name: str = Field(
        ...,
        description="Template filename or path.",
    )


class MockReq(BaseModel):
    vars: list[str] = Field(
        ...,
        description="Variables from Jinja2 AST.",
    )
    ctx: str = Field(
        "generic",
        description="Context hint (e.g., SaaS).",
    )


class DispatchReq(BaseModel):
    tpl_name: str = Field(
        ...,
        description="Template filename to render.",
    )
    mock_data: dict[str, Any] = Field(
        ...,
        description="Mock payload.",
    )
    dry_run: bool = Field(
        default=False,
        description="Set to true to render only (no email).",
    )


class TestHtmlReq(BaseModel):
    html: str = Field(
        ...,
        description="Raw Jinja2 HTML string.",
    )
    subject: str = Field(
        default="[MCP] Test",
        description="Email subject.",
    )
    dry_run: bool = Field(
        default=False,
        description="Set to true to render only (no email).",
    )

class UpdateTemplateReq(BaseModel):
    html: str = Field(
        ...,
        description="The raw HTML string to save to the default templates/email_template.html file.",
    )
