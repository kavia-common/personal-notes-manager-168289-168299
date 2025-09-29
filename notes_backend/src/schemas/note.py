from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class NoteBase(BaseModel):
    """Common fields shared by Note payloads."""

    title: str = Field(..., min_length=1, max_length=255, description="Short title for the note.")
    content: str = Field(..., min_length=1, description="Full content of the note.")


class NoteCreate(NoteBase):
    """Schema for creating a note."""
    pass


class NoteUpdate(BaseModel):
    """Schema for updating a note. Fields are optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Updated title.")
    content: Optional[str] = Field(None, min_length=1, description="Updated content.")

    @validator("title")
    def non_empty_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty.")
        return v

    @validator("content")
    def non_empty_content(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Content cannot be empty.")
        return v


class NoteOut(NoteBase):
    """Schema returned for note responses."""
    id: int = Field(..., description="Unique identifier for the note.")
    created_at: datetime = Field(..., description="Timestamp when the note was created (UTC).")
    updated_at: datetime = Field(..., description="Timestamp when the note was last updated (UTC).")

    class Config:
        from_attributes = True
