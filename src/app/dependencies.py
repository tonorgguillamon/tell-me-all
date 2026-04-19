from fastapi import Depends, HTTPException, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.auth_service import ENCRYPTION_KEY, ENCRYPTION_ALGORITHM
from storage import db_operations
from storage.db_engine import get_session
from storage.models import UserRead


class Pagination(BaseModel):
    limit: int = 50
    offset: int = 0

def get_pagination(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> Pagination:
    return Pagination(limit=limit, offset=offset)

_bearer = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, ENCRYPTION_KEY, algorithms=[ENCRYPTION_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise JWTError()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await db_operations.get_user_by_id(session, int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return UserRead.model_validate(user)