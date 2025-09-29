from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_sessionmaker
from src.schemas.note import NoteCreate, NoteUpdate, NoteOut
from src.services.notes_service import NotesService, NotFoundError

router = APIRouter(tags=["notes"])


async def get_db_session() -> AsyncSession:
    """Yield an async DB session per request."""
    SessionLocal = get_sessionmaker()
    async with SessionLocal() as session:
        yield session


def get_notes_service(session: AsyncSession = Depends(get_db_session)) -> NotesService:
    """Dependency: construct a NotesService."""
    return NotesService(session=session)


@router.post(
    "/notes",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a note",
    description="Create a new personal note with title and content.",
    responses={
        201: {"description": "Note created successfully."},
        422: {"description": "Validation error in request body."},
    },
)
# PUBLIC_INTERFACE
async def create_note(payload: NoteCreate, svc: NotesService = Depends(get_notes_service)) -> NoteOut:
    """Create a new note.

    Parameters:
    - payload: NoteCreate with required 'title' and 'content'.

    Returns:
    - NoteOut: Newly created note with id and timestamps.
    """
    note = await svc.create_note(payload)
    return NoteOut.model_validate(note)


@router.get(
    "/notes/{note_id}",
    response_model=NoteOut,
    summary="Get note by id",
    description="Retrieve a single note by its unique identifier.",
    responses={
        200: {"description": "Note retrieved successfully."},
        404: {"description": "The note was not found."},
    },
)
# PUBLIC_INTERFACE
async def get_note_by_id(
    note_id: int = Path(..., description="Unique identifier of the note.", ge=1),
    svc: NotesService = Depends(get_notes_service),
) -> NoteOut:
    """Fetch a note by its id."""
    try:
        note = await svc.get_note(note_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return NoteOut.model_validate(note)


@router.get(
    "/notes",
    response_model=List[NoteOut],
    summary="List all notes",
    description="List all notes ordered by creation date (descending).",
)
# PUBLIC_INTERFACE
async def list_notes(svc: NotesService = Depends(get_notes_service)) -> List[NoteOut]:
    """Return a list of all notes."""
    notes = await svc.list_notes()
    return [NoteOut.model_validate(n) for n in notes]


@router.put(
    "/notes/{note_id}",
    response_model=NoteOut,
    summary="Update note by id",
    description="Update the title and/or content of a note.",
    responses={
        200: {"description": "Note updated successfully."},
        404: {"description": "The note was not found."},
        422: {"description": "Validation error in request body."},
    },
)
# PUBLIC_INTERFACE
async def update_note_by_id(
    payload: NoteUpdate,
    note_id: int = Path(..., description="Unique identifier of the note.", ge=1),
    svc: NotesService = Depends(get_notes_service),
) -> NoteOut:
    """Update an existing note by id."""
    try:
        note = await svc.update_note(note_id, payload)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return NoteOut.model_validate(note)


@router.delete(
    "/notes/{note_id}",
    status_code=204,
    summary="Delete note by id",
    description="Delete a note permanently by its id.",
    responses={
        204: {"description": "Note deleted successfully."},
        404: {"description": "The note was not found."},
    },
)
# PUBLIC_INTERFACE
async def delete_note_by_id(
    note_id: int = Path(..., description="Unique identifier of the note.", ge=1),
    svc: NotesService = Depends(get_notes_service),
) -> None:
    """Delete a note by its id."""
    try:
        await svc.delete_note(note_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return None
