from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import card_service, event_service
from storage.db_engine import get_session
from storage.models import CardEventCreate, CardEventRead

router = APIRouter(tags=["events"])


@router.post(
    "/cards/{card_id}/events",
    response_model=CardEventRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_event_for_card(
    card_id: int,
    payload: CardEventCreate,
    session: AsyncSession = Depends(get_session),
) -> CardEventRead:
    card = await card_service.get_card_by_id(session, card_id)
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found",
        )

    event_payload = CardEventCreate(
        card_id=card_id,
        event_type=payload.event_type,
        summary_text=payload.summary_text,
        payload_json=payload.payload_json,
    )
    return await event_service.create_event(session, event_payload)


@router.get(
    "/cards/{card_id}/events",
    response_model=list[CardEventRead],
)
async def get_events_for_card(
    card_id: int,
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
) -> list[CardEventRead]:
    card = await card_service.get_card_by_id(session, card_id)
    if card is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Card not found",
        )

    return await event_service.get_events_for_card(
        session,
        card_id=card_id,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/events",
    response_model=list[CardEventRead],
)
async def get_all_events(
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
) -> list[CardEventRead]:
    return await event_service.get_all_events(
        session,
        limit=limit,
        offset=offset,
    )


@router.get(
    "/events/{event_id}",
    response_model=CardEventRead,
)
async def get_event(
    event_id: int,
    session: AsyncSession = Depends(get_session),
) -> CardEventRead:
    event = await event_service.get_event_by_id(session, event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return event


@router.delete(
    "/events/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_event(
    event_id: int,
    session: AsyncSession = Depends(get_session),
) -> Response:
    deleted = await event_service.delete_event(session, event_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)