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
    use_gemini: bool = Field(
        default=False,
        description="If true, use Gemini API to generate contextual mocks.",
    )
    gemini_api_key: str | None = Field(
        default=None,
        description="Gemini API key (falls back to GEMINI_API_KEY env var).",
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

class SyncAndTestReq(BaseModel):
    html: str = Field(
        ...,
        description="The raw HTML string to save and test.",
    )
    subject: str = Field(
        default="[MCP] Default Test",
        description="Email subject.",
    )
