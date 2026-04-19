from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.dependencies import get_current_user
from src.services import auth_service
from storage.db_engine import get_session
from storage.models import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=UserRead)
async def me(current_user: UserRead = Depends(get_current_user)) -> UserRead:
    return current_user


@router.post("/register", response_model=UserRead, status_code=201)
async def register(
    payload: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    try:
        return await auth_service.register(session, payload)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/login")
async def login(
    payload: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> dict:
    try:
        token = await auth_service.login(session, payload.email, payload.password)
        return {"access_token": token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))