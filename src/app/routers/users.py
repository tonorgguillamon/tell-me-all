from fastapi import APIRouter, Depends, HTTPException, Response, status
from src.app.dependencies import Pagination, get_pagination
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import user_service
from storage.db_engine import get_session
from storage.models import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    return await user_service.create_user(session, payload)


@router.get("", response_model=list[UserRead])
async def get_all_users(
    pagination: Pagination = Depends(get_pagination),
    session: AsyncSession = Depends(get_session),
) -> list[UserRead]:
    return await user_service.get_all_users(session, limit=pagination.limit, offset=pagination.offset)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    user = await user_service.get_user_by_id(session, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> Response:
    deleted = await user_service.delete_user(session, user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)