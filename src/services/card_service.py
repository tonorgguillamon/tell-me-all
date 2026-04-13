from sqlalchemy.ext.asyncio import AsyncSession

from storage import db_operations
from storage.models import CardCreate, CardRead


async def create_card(
    session: AsyncSession,
    payload: CardCreate,
) -> CardRead:
    row = await db_operations.create_card(session, payload)
    return CardRead.model_validate(row)


async def get_card_by_id(
    session: AsyncSession,
    card_id: int,
) -> CardRead | None:
    row = await db_operations.get_card_by_id(session, card_id)
    if row is None:
        return None
    return CardRead.model_validate(row)


async def get_all_cards(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[CardRead]:
    rows = await db_operations.get_all_cards(session, limit=limit, offset=offset)
    return [CardRead.model_validate(row) for row in rows]


async def get_cards_filtered(
    session: AsyncSession,
    *,
    dashboard_id: int | None = None,
    topic: str | None = None,
    title_contains: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[CardRead]:
    rows = await db_operations.get_cards_filtered(
        session,
        dashboard_id=dashboard_id,
        topic=topic,
        title_contains=title_contains,
        limit=limit,
        offset=offset,
    )
    return [CardRead.model_validate(row) for row in rows]


async def get_cards_for_dashboard(
    session: AsyncSession,
    dashboard_id: int,
    limit: int = 50,
    offset: int = 0,
) -> list[CardRead]:
    rows = await db_operations.get_cards_for_dashboard(
        session,
        dashboard_id=dashboard_id,
        limit=limit,
        offset=offset,
    )
    return [CardRead.model_validate(row) for row in rows]