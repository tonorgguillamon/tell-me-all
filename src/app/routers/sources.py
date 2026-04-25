import uuid

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.dependencies import Pagination, get_current_user, get_pagination
from src.services import card_service, source_service
from storage.db_engine import get_session
from storage.models import SourceCreate, SourceRead, SourceUpdate, UserRead

router = APIRouter(tags=["sources"])


@router.post("/sources", response_model=SourceRead, status_code=status.HTTP_201_CREATED)
async def create_source(
    payload: SourceCreate,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> SourceRead:
    return await source_service.create_source(session, current_user.id, payload)


@router.get("/sources", response_model=list[SourceRead])
async def get_sources(
    pagination: Pagination = Depends(get_pagination),
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[SourceRead]:
    return await source_service.get_sources_for_user(
        session, current_user.id, limit=pagination.limit, offset=pagination.offset
    )


@router.get("/sources/{source_id}", response_model=SourceRead)
async def get_source(
    source_id: uuid.UUID,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> SourceRead:
    source = await source_service.get_source_by_id(session, source_id)
    if source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    return source


@router.post("/cards/{card_id}/sources/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def attach_source_to_card(
    card_id: uuid.UUID,
    source_id: uuid.UUID,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Response:
    card = await card_service.get_card_by_id(session, card_id)
    source = await source_service.get_source_by_id(session, source_id)
    if card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    if source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    await source_service.attach_source_to_card(session, card_id, source_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/sources/{source_id}", response_model=SourceRead)
async def update_source(
    source_id: uuid.UUID,
    payload: SourceUpdate,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> SourceRead:
    source = await source_service.update_source(session, source_id, payload)
    if source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    return source


@router.delete("/sources/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(
    source_id: uuid.UUID,
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Response:
    deleted = await source_service.delete_source(session, source_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/cards/{card_id}/sources", response_model=list[SourceRead])
async def get_sources_for_card(
    card_id: uuid.UUID,
    pagination: Pagination = Depends(get_pagination),
    current_user: UserRead = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[SourceRead]:
    card = await card_service.get_card_by_id(session, card_id)
    if card is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
    return await source_service.get_sources_for_card(session, card_id, limit=pagination.limit, offset=pagination.offset)