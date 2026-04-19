from datetime import datetime, timedelta, timezone

from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.auth_utils import hash_password, verify_password
from storage import db_operations
from storage.models import UserCreate, UserRead

from dotenv import load_dotenv
import os
load_dotenv()

ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', None)
if not ENCRYPTION_KEY:
    raise RuntimeError("ENCRYPTION_KEY environment variable is not set")

ENCRYPTION_ALGORITHM = os.getenv('HASH_ENCRYPTION', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

async def register(session: AsyncSession, payload: UserCreate) -> UserRead:
    existing = await db_operations.get_user_by_email(session, payload.email)
    if existing:
        raise ValueError("Email already registered")
    hashed = hash_password(payload.password)
    row = await db_operations.create_user(session, payload, hashed_password=hashed)
    return UserRead.model_validate(row)


async def login(session: AsyncSession, email: str, password: str) -> str:
    user = await db_operations.get_user_by_email(session, email)
    if not user or not verify_password(password, user.hashed_password):
        raise ValueError("Invalid credentials")
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode({"sub": str(user.id), "exp": expire}, ENCRYPTION_KEY, algorithm=ENCRYPTION_ALGORITHM)
    return token