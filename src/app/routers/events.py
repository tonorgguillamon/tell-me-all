from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.dependencies import Pagination, get_current_user, get_pagination
from src.services import card_service, event_service, source_service
from storage.db_engine import get_session
from storage.models import SourceEventCreate, SourceEventRead, UserRead

router = APIRouter(tags=["events"])


@router.get("/cards/{card_id}/events", response_model=list[SourceEventRead])
async def get_events_for_card(
    card_id: int,
    pagination: Pagination = Depends(get_pagination),
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[SourceEventRead]:
    card = await card_service.get_card_by_id(session, card_id)
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found",
        )

    return await event_service.get_events_for_card(
        session,
        card_id=card_id,
        limit=pagination.limit,
        offset=pagination.offset,
    )

@router.get("/sources/{source_id}/events", response_model=list[SourceEventRead])
async def get_events_for_source(
    source_id: int,
    pagination: Pagination = Depends(get_pagination),
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[SourceEventRead]:
    source = await source_service.get_source_by_id(session, source_id)
    if source is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source not found",
        )

    return await event_service.get_events_filtered(
        session,
        source_id=source_id,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.post("/sources/{source_id}/events", response_model=SourceEventRead, status_code=status.HTTP_201_CREATED)
async def ingest_event_for_source(
    source_id: int,
    payload: SourceEventCreate,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> SourceEventRead:
    source = await source_service.get_source_by_id(session, source_id)
    if source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    return await event_service.create_event(session, SourceEventCreate(
        source_id=source_id,
        **payload.model_dump(exclude={"source_id"}),
    ))


@router.get("/events", response_model=list[SourceEventRead])
async def get_all_events(
    pagination: Pagination = Depends(get_pagination),
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[SourceEventRead]:
    return await event_service.get_all_events(
        session,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get("/events/{event_id}", response_model=SourceEventRead)
async def get_event(
    event_id: int,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> SourceEventRead:
    event = await event_service.get_event_by_id(session, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return event


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Response:
    deleted = await event_service.delete_event(session, event_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)