from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from storage.models import Card, CardCreate, CardEvent, CardEventCreate, CardSource, Dashboard, DashboardCreate, Source, SourceCreate, User, UserCreate


# -------------------------
# Write operations
# -------------------------

async def create_user(
    session: AsyncSession,
    payload: UserCreate,
) -> User:
    row = User(email=payload.email)
    session.add(row)
    await session.flush()
    await session.refresh(row)
    return row


async def create_dashboard(
    session: AsyncSession,
    user_id: int,
    payload: DashboardCreate,
) -> Dashboard:
    row = Dashboard(user_id=user_id, name=payload.name)
    session.add(row)
    await session.flush()
    await session.refresh(row)
    return row


async def create_card(
    session: AsyncSession,
    payload: CardCreate,
) -> Card:
    row = Card(
        dashboard_id=payload.dashboard_id,
        title=payload.title,
        topic=payload.topic,
    )
    session.add(row)
    await session.flush()
    await session.refresh(row)
    return row


async def create_event(
    session: AsyncSession,
    payload: CardEventCreate,
) -> CardEvent:
    row = CardEvent(
        source_id=payload.source_id,
        event_type=payload.event_type,
        summary_text=payload.summary_text,
        payload_json=payload.payload_json,
    )
    session.add(row)
    await session.flush()
    await session.refresh(row)
    return row


async def create_source(
    session: AsyncSession,
    user_id: int,
    payload: SourceCreate,
) -> Source:
    row = Source(
        user_id=user_id,
        source_type=payload.source_type,
        name=payload.name,
        config_json=payload.config_json,
    )
    session.add(row)
    await session.flush()
    await session.refresh(row)
    return row


async def attach_source_to_card(
    session: AsyncSession,
    card_id: int,
    source_id: int,
) -> CardSource:
    row = CardSource(card_id=card_id, source_id=source_id)
    session.add(row)
    await session.flush()
    await session.refresh(row)
    return row


# -------------------------
# User queries
# -------------------------

async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    return await session.get(User, user_id)


async def get_all_users(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[User]:
    stmt = (
        select(User)
        .order_by(User.id)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_users_filtered(
    session: AsyncSession,
    *,
    email_contains: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[User]:
    stmt = select(User)

    if email_contains:
        stmt = stmt.where(User.email.ilike(f"%{email_contains}%"))

    stmt = stmt.order_by(User.id).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


# -------------------------
# Dashboard queries
# -------------------------

async def get_dashboard_by_id(
    session: AsyncSession,
    dashboard_id: int,
) -> Dashboard | None:
    return await session.get(Dashboard, dashboard_id)


async def get_all_dashboards(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[Dashboard]:
    stmt = (
        select(Dashboard)
        .order_by(Dashboard.id)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_dashboards_filtered(
    session: AsyncSession,
    *,
    user_id: int | None = None,
    name_contains: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Dashboard]:
    stmt = select(Dashboard)

    if user_id is not None:
        stmt = stmt.where(Dashboard.user_id == user_id)
    if name_contains:
        stmt = stmt.where(Dashboard.name.ilike(f"%{name_contains}%"))

    stmt = stmt.order_by(Dashboard.id).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


# -------------------------
# Card queries
# -------------------------

async def get_card_by_id(
    session: AsyncSession,
    card_id: int,
) -> Card | None:
    return await session.get(Card, card_id)


async def get_all_cards(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[Card]:
    stmt = (
        select(Card)
        .order_by(Card.id)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_cards_filtered(
    session: AsyncSession,
    *,
    dashboard_id: int | None = None,
    topic: str | None = None,
    title_contains: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Card]:
    stmt = select(Card)

    if dashboard_id is not None:
        stmt = stmt.where(Card.dashboard_id == dashboard_id)
    if topic:
        stmt = stmt.where(Card.topic.ilike(f"%{topic}%"))
    if title_contains:
        stmt = stmt.where(Card.title.ilike(f"%{title_contains}%"))

    stmt = stmt.order_by(Card.id).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


# -------------------------
# Event queries
# -------------------------

async def get_event_by_id(
    session: AsyncSession,
    event_id: int,
) -> CardEvent | None:
    return await session.get(CardEvent, event_id)


async def get_all_events(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[CardEvent]:
    stmt = (
        select(CardEvent)
        .order_by(CardEvent.occurred_at.desc(), CardEvent.id.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_events_filtered(
    session: AsyncSession,
    *,
    source_id: int | None = None,
    event_type: str | None = None,
    from_occurred_at: datetime | None = None,
    to_occurred_at: datetime | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[CardEvent]:
    stmt = select(CardEvent)

    if source_id is not None:
        stmt = stmt.where(CardEvent.source_id == source_id)
    if event_type:
        stmt = stmt.where(CardEvent.event_type == event_type)
    if from_occurred_at is not None:
        stmt = stmt.where(CardEvent.occurred_at >= from_occurred_at)
    if to_occurred_at is not None:
        stmt = stmt.where(CardEvent.occurred_at <= to_occurred_at)

    stmt = stmt.order_by(CardEvent.occurred_at.desc(), CardEvent.id.desc()).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


# -------------------------
# Associations
# -------------------------

async def get_dashboards_for_user(
    session: AsyncSession,
    user_id: int,
    limit: int = 50,
    offset: int = 0,
) -> list[Dashboard]:
    stmt = (
        select(Dashboard)
        .where(Dashboard.user_id == user_id)
        .order_by(Dashboard.id)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_cards_for_dashboard(
    session: AsyncSession,
    dashboard_id: int,
    limit: int = 50,
    offset: int = 0,
) -> list[Card]:
    stmt = (
        select(Card)
        .where(Card.dashboard_id == dashboard_id)
        .order_by(Card.id)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_events_for_card(
    session: AsyncSession,
    card_id: int,
    limit: int = 50,
    offset: int = 0,
) -> list[CardEvent]:
    stmt = (
        select(CardEvent)
        .join(CardSource, CardSource.source_id == CardEvent.source_id)
        .where(CardSource.card_id == card_id)
        .order_by(CardEvent.occurred_at.desc(), CardEvent.id.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_source_by_id(
    session: AsyncSession,
    source_id: int,
) -> Source | None:
    return await session.get(Source, source_id)


async def get_all_sources(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[Source]:
    stmt = select(Source).order_by(Source.id).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_sources_filtered(
    session: AsyncSession,
    *,
    user_id: int | None = None,
    source_type: str | None = None,
    name_contains: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Source]:
    stmt = select(Source)

    if user_id is not None:
        stmt = stmt.where(Source.user_id == user_id)
    if source_type:
        stmt = stmt.where(Source.source_type == source_type)
    if name_contains:
        stmt = stmt.where(Source.name.ilike(f"%{name_contains}%"))

    stmt = stmt.order_by(Source.id).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_sources_for_user(
    session: AsyncSession,
    user_id: int,
    limit: int = 50,
    offset: int = 0,
) -> list[Source]:
    stmt = (
        select(Source)
        .where(Source.user_id == user_id)
        .order_by(Source.id)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_sources_for_card(
    session: AsyncSession,
    card_id: int,
    limit: int = 50,
    offset: int = 0,
) -> list[Source]:
    stmt = (
        select(Source)
        .join(CardSource, CardSource.source_id == Source.id)
        .where(CardSource.card_id == card_id)
        .order_by(Source.id)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())