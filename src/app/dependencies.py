import uuid

from fastapi import Depends, HTTPException, Query, Request
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.auth_service import ENCRYPTION_KEY, ENCRYPTION_ALGORITHM
from storage import db_operations
from storage.db_engine import get_session
from storage.models import UserRead

_COOKIE_NAME = "access_token"


class Pagination(BaseModel):
    limit: int = 50
    offset: int = 0

def get_pagination(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> Pagination:
    return Pagination(limit=limit, offset=offset)


async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    token = request.cookies.get(_COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, ENCRYPTION_KEY, algorithms=[ENCRYPTION_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise JWTError()
        user_uuid = uuid.UUID(user_id)
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await db_operations.get_user_by_id(session, user_uuid)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return UserRead.model_validate(user)