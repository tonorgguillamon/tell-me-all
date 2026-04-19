from sqlalchemy.ext.asyncio import AsyncSession

from storage import db_operations
from storage.models import SourceCreate, SourceRead


async def create_source(
	session: AsyncSession,
	user_id: int,
	payload: SourceCreate,
) -> SourceRead:
	row = await db_operations.create_source(session, user_id, payload)
	return SourceRead.model_validate(row)


async def get_source_by_id(
	session: AsyncSession,
	source_id: int,
) -> SourceRead | None:
	row = await db_operations.get_source_by_id(session, source_id)
	if row is None:
		return None
	return SourceRead.model_validate(row)


async def get_all_sources(
	session: AsyncSession,
	limit: int = 50,
	offset: int = 0,
) -> list[SourceRead]:
	rows = await db_operations.get_all_sources(session, limit=limit, offset=offset)
	return [SourceRead.model_validate(row) for row in rows]


async def get_sources_for_user(
	session: AsyncSession,
	user_id: int,
	limit: int = 50,
	offset: int = 0,
) -> list[SourceRead]:
	rows = await db_operations.get_sources_for_user(session, user_id, limit=limit, offset=offset)
	return [SourceRead.model_validate(row) for row in rows]


async def get_sources_for_card(
	session: AsyncSession,
	card_id: int,
	limit: int = 50,
	offset: int = 0,
) -> list[SourceRead]:
	rows = await db_operations.get_sources_for_card(session, card_id, limit=limit, offset=offset)
	return [SourceRead.model_validate(row) for row in rows]


async def attach_source_to_card(
	session: AsyncSession,
	card_id: int,
	source_id: int,
) -> None:
	await db_operations.attach_source_to_card(session, card_id, source_id)
