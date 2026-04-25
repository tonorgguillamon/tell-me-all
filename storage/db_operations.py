import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from storage.models import Card, CardCreate, CardSource, Dashboard, DashboardCreate, Source, SourceCreate, SourceUpdate, SourceEvent, SourceEventCreate, User, UserCreate


async def create_user(
    session: AsyncSession,
    payload: UserCreate,
    hashed_password: str
) -> User:
    row = User(email=payload.email, hashed_password=hashed_password)
    session.add(row)
    await session.flush()
    await session.refresh(row)
    return row


async def create_dashboard(
    session: AsyncSession,
    user_id: uuid.UUID,
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
    payload: SourceEventCreate,
) -> SourceEvent:
    row = SourceEvent(
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
    user_id: uuid.UUID,
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
    card_id: uuid.UUID,
    source_id: uuid.UUID,
) -> CardSource:
    row = CardSource(card_id=card_id, source_id=source_id)
    session.add(row)
    await session.flush()
    await session.refresh(row)
    return row


async def get_user_by_id(
    session: AsyncSession,
    user_id: uuid.UUID,
) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_email(
    session: AsyncSession,
    email: str,
) -> User | None:
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_all_users(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[User]:
    stmt = (
        select(User)
        .order_by(User.email)
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

    stmt = stmt.order_by(User.email).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


# -------------------------
# Dashboard queries
# -------------------------

async def get_dashboard_by_id(
    session: AsyncSession,
    dashboard_id: uuid.UUID,
) -> Dashboard | None:
    return await session.get(Dashboard, dashboard_id)


async def get_all_dashboards(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[Dashboard]:
    stmt = (
        select(Dashboard)
        .order_by(Dashboard.name)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_dashboards_filtered(
    session: AsyncSession,
    *,
    user_id: uuid.UUID | None = None,
    name_contains: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[Dashboard]:
    stmt = select(Dashboard)

    if user_id is not None:
        stmt = stmt.where(Dashboard.user_id == user_id)
    if name_contains:
        stmt = stmt.where(Dashboard.name.ilike(f"%{name_contains}%"))

    stmt = stmt.order_by(Dashboard.name).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


# -------------------------
# Card queries
# -------------------------

async def get_card_by_id(
    session: AsyncSession,
    card_id: uuid.UUID,
) -> Card | None:
    return await session.get(Card, card_id)


async def get_all_cards(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[Card]:
    stmt = (
        select(Card)
        .order_by(Card.title)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_cards_filtered(
    session: AsyncSession,
    *,
    dashboard_id: uuid.UUID | None = None,
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

    stmt = stmt.order_by(Card.title).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


# -------------------------
# Event queries
# -------------------------

async def get_event_by_id(
    session: AsyncSession,
    event_id: uuid.UUID,
) -> SourceEvent | None:
    return await session.get(SourceEvent, event_id)


async def get_all_events(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[SourceEvent]:
    stmt = (
        select(SourceEvent)
        .order_by(SourceEvent.occurred_at.desc(), SourceEvent.id.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_events_filtered(
    session: AsyncSession,
    *,
    source_id: uuid.UUID | None = None,
    event_type: str | None = None,
    from_occurred_at: datetime | None = None,
    to_occurred_at: datetime | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[SourceEvent]:
    stmt = select(SourceEvent)

    if source_id is not None:
        stmt = stmt.where(SourceEvent.source_id == source_id)
    if event_type:
        stmt = stmt.where(SourceEvent.event_type == event_type)
    if from_occurred_at is not None:
        stmt = stmt.where(SourceEvent.occurred_at >= from_occurred_at)
    if to_occurred_at is not None:
        stmt = stmt.where(SourceEvent.occurred_at <= to_occurred_at)

    stmt = stmt.order_by(SourceEvent.occurred_at.desc(), SourceEvent.id.desc()).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


# -------------------------
# Associations
# -------------------------

async def get_dashboards_for_user(
    session: AsyncSession,
    user_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
) -> list[Dashboard]:
    stmt = (
        select(Dashboard)
        .where(Dashboard.user_id == user_id)
        .order_by(Dashboard.name)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_cards_for_dashboard(
    session: AsyncSession,
    dashboard_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
) -> list[Card]:
    stmt = (
        select(Card)
        .where(Card.dashboard_id == dashboard_id)
        .order_by(Card.title)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_events_for_card(
    session: AsyncSession,
    card_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
) -> list[SourceEvent]:
    stmt = (
        select(SourceEvent)
        .join(CardSource, CardSource.source_id == SourceEvent.source_id)
        .where(CardSource.card_id == card_id)
        .order_by(SourceEvent.occurred_at.desc(), SourceEvent.id.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_source_by_id(
    session: AsyncSession,
    source_id: uuid.UUID,
) -> Source | None:
    return await session.get(Source, source_id)


async def get_all_sources(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[Source]:
    stmt = select(Source).order_by(Source.name).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_sources_filtered(
    session: AsyncSession,
    *,
    user_id: uuid.UUID | None = None,
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

    stmt = stmt.order_by(Source.name).limit(limit).offset(offset)
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_sources_for_user(
    session: AsyncSession,
    user_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
) -> list[Source]:
    stmt = (
        select(Source)
        .where(Source.user_id == user_id)
        .order_by(Source.name)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_sources_for_card(
    session: AsyncSession,
    card_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
) -> list[Source]:
    stmt = (
        select(Source)
        .join(CardSource, CardSource.source_id == Source.id)
        .where(CardSource.card_id == card_id)
        .order_by(Source.name)
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


async def update_source(
    session: AsyncSession,
    source_id: uuid.UUID,
    payload: SourceUpdate,
) -> Source | None:
    row = await session.get(Source, source_id)
    if row is None:
        return None
    if payload.name is not None:
        row.name = payload.name
    if payload.source_type is not None:
        row.source_type = payload.source_type
    if payload.config_json is not None:
        row.config_json = payload.config_json
    await session.flush()
    await session.refresh(row)
    return row


async def delete_source(session: AsyncSession, source_id: uuid.UUID) -> bool:
    row = await session.get(Source, source_id)
    if row is None:
        return False
    await session.delete(row)
    await session.flush()
    return True


async def delete_user(session: AsyncSession, user_id: uuid.UUID) -> bool:
    row = await session.get(User, user_id)
    if row is None:
        return False
    await session.delete(row)
    await session.flush()
    return True


async def delete_dashboard(session: AsyncSession, dashboard_id: uuid.UUID) -> bool:
    row = await session.get(Dashboard, dashboard_id)
    if row is None:
        return False
    await session.delete(row)
    await session.flush()
    return True


async def delete_card(session: AsyncSession, card_id: uuid.UUID) -> bool:
    row = await session.get(Card, card_id)
    if row is None:
        return False
    await session.delete(row)
    await session.flush()
    return True


async def delete_event(session: AsyncSession, event_id: uuid.UUID) -> bool:
    row = await session.get(SourceEvent, event_id)
    if row is None:
        return False
    await session.delete(row)
    await session.flush()
    return True