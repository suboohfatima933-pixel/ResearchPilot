from datetime import datetime
from typing import List

from pydantic import BaseModel


class Paper(BaseModel):
    """Standard paper model used throughout ResearchPilot."""

    title: str
    authors: List[str]
    abstract: str
    published: datetime
    pdf_url: str
    arxiv_url: str
    categories: List[str]