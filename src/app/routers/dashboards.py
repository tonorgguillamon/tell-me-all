import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.dependencies import Pagination, get_current_user, get_pagination
from src.services import dashboard_service
from storage.db_engine import get_session
from storage.models import DashboardCreate, DashboardRead, UserRead

router = APIRouter(tags=["dashboards"])


@router.post("/dashboards", response_model=DashboardRead, status_code=status.HTTP_201_CREATED)
async def create_dashboard(
    payload: DashboardCreate,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> DashboardRead:
    return await dashboard_service.create_dashboard(
        session,
        user_id=current_user.id,
        payload=payload,
    )


@router.get("/dashboards", response_model=list[DashboardRead])
async def get_dashboards(
    pagination: Pagination = Depends(get_pagination),
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[DashboardRead]:
    return await dashboard_service.get_dashboards_for_user(
        session,
        user_id=current_user.id,
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get("/dashboards/{dashboard_id}", response_model=DashboardRead)
async def get_dashboard(
    dashboard_id: uuid.UUID,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> DashboardRead:
    dashboard = await dashboard_service.get_dashboard_by_id(session, dashboard_id)
    if dashboard is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard not found")
    return dashboard


@router.delete("/dashboards/{dashboard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dashboard(
    dashboard_id: uuid.UUID,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Response:
    deleted = await dashboard_service.delete_dashboard(session, dashboard_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)