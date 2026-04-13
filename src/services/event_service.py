from sqlalchemy.ext.asyncio import AsyncSession

from storage import db_operations
from storage.models import CardEventCreate, CardEventRead


async def create_event(
    session: AsyncSession,
    payload: CardEventCreate,
) -> CardEventRead:
    row = await db_operations.create_event(session, payload)
    return CardEventRead.model_validate(row)


async def get_event_by_id(
    session: AsyncSession,
    event_id: int,
) -> CardEventRead | None:
    row = await db_operations.get_event_by_id(session, event_id)
    if row is None:
        return None
    return CardEventRead.model_validate(row)


async def get_all_events(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[CardEventRead]:
    rows = await db_operations.get_all_events(session, limit=limit, offset=offset)
    return [CardEventRead.model_validate(row) for row in rows]


async def get_events_filtered(
    session: AsyncSession,
    *,
    card_id: int | None = None,
    event_type: str | None = None,
    from_occurred_at=None,
    to_occurred_at=None,
    unassociated_only: bool = False,
    limit: int = 50,
    offset: int = 0,
) -> list[CardEventRead]:
    rows = await db_operations.get_events_filtered(
        session,
        card_id=card_id,
        event_type=event_type,
        from_occurred_at=from_occurred_at,
        to_occurred_at=to_occurred_at,
        unassociated_only=unassociated_only,
        limit=limit,
        offset=offset,
    )
    return [CardEventRead.model_validate(row) for row in rows]


async def get_events_for_card(
    session: AsyncSession,
    card_id: int,
    limit: int = 50,
    offset: int = 0,
) -> list[CardEventRead]:
    rows = await db_operations.get_events_for_card(
        session,
        card_id=card_id,
        limit=limit,
        offset=offset,
    )
    return [CardEventRead.model_validate(row) for row in rows]