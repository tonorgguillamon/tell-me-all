from sqlalchemy.ext.asyncio import AsyncSession

from storage import db_operations
from storage.models import DashboardCreate, DashboardRead


async def create_dashboard(
    session: AsyncSession,
    user_id: int,
    payload: DashboardCreate,
) -> DashboardRead:
    row = await db_operations.create_dashboard(session, user_id, payload)
    return DashboardRead.model_validate(row)


async def get_dashboard_by_id(
    session: AsyncSession,
    dashboard_id: int,
) -> DashboardRead | None:
    row = await db_operations.get_dashboard_by_id(session, dashboard_id)
    if row is None:
        return None
    return DashboardRead.model_validate(row)


async def get_all_dashboards(
    session: AsyncSession,
    limit: int = 50,
    offset: int = 0,
) -> list[DashboardRead]:
    rows = await db_operations.get_all_dashboards(session, limit=limit, offset=offset)
    return [DashboardRead.model_validate(row) for row in rows]


async def get_dashboards_filtered(
    session: AsyncSession,
    *,
    user_id: int | None = None,
    name_contains: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> list[DashboardRead]:
    rows = await db_operations.get_dashboards_filtered(
        session,
        user_id=user_id,
        name_contains=name_contains,
        limit=limit,
        offset=offset,
    )
    return [DashboardRead.model_validate(row) for row in rows]


async def get_dashboards_for_user(
    session: AsyncSession,
    user_id: int,
    limit: int = 50,
    offset: int = 0,
) -> list[DashboardRead]:
    rows = await db_operations.get_dashboards_for_user(
        session,
        user_id=user_id,
        limit=limit,
        offset=offset,
    )
    return [DashboardRead.model_validate(row) for row in rows]


async def delete_dashboard(session: AsyncSession, dashboard_id: int) -> bool:
    return await db_operations.delete_dashboard(session, dashboard_id)