
from sqlalchemy.ext.asyncio import AsyncSession

from storage import db_operations
from storage.models import UserCreate, UserRead


async def create_user(
    session: AsyncSession,
    payload: UserCreate,
) -> UserRead:
    row = await db_operations.create_user(session, payload)
    return UserRead.model_validate(row)


async def get_user_by_id(
    session: AsyncSession,
    user_id: int,
) -> UserRead | None:
    row = await db_operations.get_user_by_id(session, user_id)
    if row is None:
        return None
    return UserRead.model_validate(row)


async def get_all_users(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[UserRead]:
    rows = await db_operations.get_all_users(session, limit=limit, offset=offset)
    return [UserRead.model_validate(row) for row in rows]


async def get_users_filtered(
    session: AsyncSession,
    *, # enforce named arguments
    email_contains: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[UserRead]:
    rows = await db_operations.get_users_filtered(
        session,
        email_contains=email_contains,
        limit=limit,
        offset=offset,
    )
    return [UserRead.model_validate(row) for row in rows]