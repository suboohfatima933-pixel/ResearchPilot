from pydantic import BaseModel, Field


class ResearchInsights(BaseModel):
    """Represents AI-generated insights from a research paper."""

    document_id: str
    document_name: str
    executive_summary: str
    research_problem: str
    objectives: list[str] = Field(
        default_factory=list
    )
    methodology: str = ""
    key_findings: list[str] = Field(
        default_factory=list
    )
    limitations: list[str] = Field(
        default_factory=list
    )
    research_gaps: list[str] = Field(
        default_factory=list
    )
    practical_impact: str = ""
    key_takeaways: list[str] = Field(
        default_factory=list
    )