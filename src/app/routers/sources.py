from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import card_service, source_service, user_service
from storage.db_engine import get_session
from storage.models import SourceCreate, SourceIngestRequest, SourceIngestResponse, SourceRead

router = APIRouter(tags=["sources"])


@router.post("/users/{user_id}/sources", response_model=SourceRead, status_code=status.HTTP_201_CREATED)
async def create_source_for_user(
	user_id: int,
	payload: SourceCreate,
	session: AsyncSession = Depends(get_session),
) -> SourceRead:
	user = await user_service.get_user_by_id(session, user_id)
	if user is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
	return await source_service.create_source(session, user_id, payload)


@router.get("/users/{user_id}/sources", response_model=list[SourceRead])
async def get_sources_for_user(
	user_id: int,
	limit: int = 50,
	offset: int = 0,
	session: AsyncSession = Depends(get_session),
) -> list[SourceRead]:
	user = await user_service.get_user_by_id(session, user_id)
	if user is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
	return await source_service.get_sources_for_user(session, user_id, limit=limit, offset=offset)


@router.post("/cards/{card_id}/sources/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
async def attach_source_to_card(
	card_id: int,
	source_id: int,
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


@router.get("/cards/{card_id}/sources", response_model=list[SourceRead])
async def get_sources_for_card(
	card_id: int,
	limit: int = 50,
	offset: int = 0,
	session: AsyncSession = Depends(get_session),
) -> list[SourceRead]:
	card = await card_service.get_card_by_id(session, card_id)
	if card is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Card not found")
	return await source_service.get_sources_for_card(session, card_id, limit=limit, offset=offset)


@router.post("/sources/{source_id}/events", response_model=SourceIngestResponse, status_code=status.HTTP_201_CREATED)
async def ingest_event_for_source(
	source_id: int,
	payload: SourceIngestRequest,
	session: AsyncSession = Depends(get_session),
) -> SourceIngestResponse:
	source = await source_service.get_source_by_id(session, source_id)
	if source is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Source not found")

	ingest_payload = SourceIngestRequest(
		source_id=source_id,
		event_type=payload.event_type,
		summary_text=payload.summary_text,
		payload_json=payload.payload_json,
	)
	return await source_service.ingest_source_event(session, ingest_payload)
