from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.note import Note


class NotesRepository:
    """Data access layer for notes."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, title: str, content: str) -> Note:
        note = Note(title=title, content=content)
        self.session.add(note)
        await self.session.flush()  # Assigns PK
        await self.session.refresh(note)
        return note

    async def get(self, note_id: int) -> Optional[Note]:
        stmt = select(Note).where(Note.id == note_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self) -> List[Note]:
        stmt = select(Note).order_by(Note.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, note: Note, *, title: Optional[str], content: Optional[str]) -> Note:
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        self.session.add(note)
        await self.session.flush()
        await self.session.refresh(note)
        return note

    async def delete(self, note: Note) -> None:
        await self.session.delete(note)
        # flush will be managed by service commit
