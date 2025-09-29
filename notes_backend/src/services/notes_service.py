from __future__ import annotations

from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.notes_repository import NotesRepository
from src.schemas.note import NoteCreate, NoteUpdate
from src.models.note import Note


class NotFoundError(Exception):
    """Raised when a note is not found."""


class NotesService:
    """Business logic for managing notes."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = NotesRepository(session)

    # PUBLIC_INTERFACE
    async def create_note(self, payload: NoteCreate) -> Note:
        """Create a new note from the provided payload."""
        async with self.session.begin():
            note = await self.repo.create(title=payload.title.strip(), content=payload.content.strip())
        return note

    # PUBLIC_INTERFACE
    async def get_note(self, note_id: int) -> Note:
        """Get a note by id or raise NotFoundError."""
        async with self.session.begin():
            note = await self.repo.get(note_id)
        if note is None:
            raise NotFoundError(f"Note with id {note_id} not found")
        return note

    # PUBLIC_INTERFACE
    async def list_notes(self) -> List[Note]:
        """List all notes ordered by creation date (desc)."""
        async with self.session.begin():
            notes = await self.repo.list()
        return notes

    # PUBLIC_INTERFACE
    async def update_note(self, note_id: int, payload: NoteUpdate) -> Note:
        """Update fields of a note by id or raise NotFoundError."""
        async with self.session.begin():
            note = await self.repo.get(note_id)
            if note is None:
                raise NotFoundError(f"Note with id {note_id} not found")
            updated = await self.repo.update(
                note,
                title=payload.title.strip() if payload.title is not None else None,
                content=payload.content.strip() if payload.content is not None else None,
            )
        return updated

    # PUBLIC_INTERFACE
    async def delete_note(self, note_id: int) -> None:
        """Delete a note by id or raise NotFoundError."""
        async with self.session.begin():
            note = await self.repo.get(note_id)
            if note is None:
                raise NotFoundError(f"Note with id {note_id} not found")
            await self.repo.delete(note)
