
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import card_service, dashboard_service
from storage.db_engine import get_session
from storage.models import CardCreate, CardRead

router = APIRouter(tags=["cards"])


@router.post(
    "/dashboards/{dashboard_id}/cards",
    response_model=CardRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_card_for_dashboard(
    dashboard_id: int,
    payload: CardCreate,
    session: AsyncSession = Depends(get_session),
) -> CardRead:
    dashboard = await dashboard_service.get_dashboard_by_id(session, dashboard_id)
    if dashboard is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard not found")

    card_payload = CardCreate(
        dashboard_id=dashboard_id,
        title=payload.title,
        topic=payload.topic,
    )
    return await card_service.create_card(session, card_payload)


@router.get("/dashboards/{dashboard_id}/cards", response_model=list[CardRead])
async def get_cards_for_dashboard(
    dashboard_id: int,
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
) -> list[CardRead]:
    dashboard = await dashboard_service.get_dashboard_by_id(session, dashboard_id)
    if dashboard is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dashboard not found")

    return await card_service.get_cards_for_dashboard(
        session,
        dashboard_id=dashboard_id,
        limit=limit,
        offset=offset,
    )


@router.get("/cards/{card_id}", response_model=CardRead)
async def get_card(
    card_id: int,
    session: AsyncSession = Depends(get_session),
) -> CardRead:
    card = await card_service.get_card_by_id(session, card_id)
    if card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return card


@router.delete("/cards/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(
    card_id: int,
    session: AsyncSession = Depends(get_session),
) -> Response:
    deleted = await card_service.delete_card(session, card_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)