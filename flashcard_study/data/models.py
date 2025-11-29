"""Pydantic models for flash card data structures."""

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field
from uuid import UUID


class ReviewHistory(BaseModel):
    """Record of a single review session for a card."""
    date: datetime
    score: float
    interval_days: float


class FlashCard(BaseModel):
    """A single flash card with spaced repetition metadata."""
    id: UUID
    type: Literal["qa", "cloze", "multiple_choice"]
    question: str
    answer: str
    tags: list[str] = Field(default_factory=list)
    options: Optional[list[str]] = None  # For multiple_choice type
    created_at: datetime
    last_reviewed: Optional[datetime] = None
    next_review: datetime
    ease_factor: float = 2.5
    interval_days: float = 0.0
    review_count: int = 0
    review_history: list[ReviewHistory] = Field(default_factory=list)


class FlashCardDatabase(BaseModel):
    """Container for all flash cards."""
    version: str = "1.0"
    cards: list[FlashCard] = Field(default_factory=list)
