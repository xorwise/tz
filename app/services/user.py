import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from core.settings import settings
from core.database import get_session
from datetime import datetime, timedelta, UTC
import jwt
import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/token")


async def get_user_by_phone(db: AsyncSession, phone: str) -> models.User | None:
    result = await db.execute(select(models.User).where(models.User.phone == phone))
    return result.scalar()


async def get_user_by_id(db: AsyncSession, user_id: str) -> models.User | None:
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalar()


def create_access_token(data: dict, expiry: timedelta):
    to_encode = data.copy()
    expire = datetime.now(UTC) + expiry
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_TOKEN_SECRET, algorithm="HS256")
    return encoded_jwt


def create_refresh_token(data: dict, expiry: timedelta):
    to_encode = data.copy()
    expire = datetime.now(UTC) + expiry
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.REFRESH_TOKEN_SECRET, algorithm="HS256"
    )
    return encoded_jwt


async def verify_refresh_token(session: AsyncSession, token: str) -> models.User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.REFRESH_TOKEN_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = await get_user_by_id(session, user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_user(
    session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.ACCESS_TOKEN_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = await get_user_by_id(session, user_id)
    if user is None:
        raise credentials_exception
    return user


async def create_user(session: AsyncSession, phone: str) -> models.User:
    user = models.User(id=uuid.uuid4(), phone=phone)
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists")
    await session.refresh(user)
    return user
