from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import dashboard_service, user_service
from storage.db_engine import get_session
from storage.models import DashboardCreate, DashboardRead

router = APIRouter(tags=["dashboards"])


@router.post(
    "/users/{user_id}/dashboards",
    response_model=DashboardRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_dashboard_for_user(
    user_id: int,
    payload: DashboardCreate,
    session: AsyncSession = Depends(get_session),
) -> DashboardRead:
    user = await user_service.get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return await dashboard_service.create_dashboard(
        session,
        user_id=user_id,
        payload=payload,
    )


@router.get("/users/{user_id}/dashboards", response_model=list[DashboardRead])
async def get_dashboards_for_user(
    user_id: int,
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
) -> list[DashboardRead]:
    user = await user_service.get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return await dashboard_service.get_dashboards_for_user(
        session,
        user_id=user_id,
        limit=limit,
        offset=offset,
    )


@router.get("/dashboards", response_model=list[DashboardRead])
async def get_all_dashboards(
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
) -> list[DashboardRead]:
    return await dashboard_service.get_all_dashboards(
        session,
        limit=limit,
        offset=offset,
    )


@router.get("/dashboards/{dashboard_id}", response_model=DashboardRead)
async def get_dashboard(
    dashboard_id: int,
    session: AsyncSession = Depends(get_session),
) -> DashboardRead:
    dashboard = await dashboard_service.get_dashboard_by_id(session, dashboard_id)
    if dashboard is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard not found")
    return dashboard


@router.delete("/dashboards/{dashboard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dashboard(
    dashboard_id: int,
    session: AsyncSession = Depends(get_session),
) -> Response:
    deleted = await dashboard_service.delete_dashboard(session, dashboard_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)