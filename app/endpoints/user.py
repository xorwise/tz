from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import models
from schemas.user import LoginResponse, LoginRequest, RefreshRequest, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
import services
from core.settings import settings
from core.database import get_session

user_router = APIRouter(
    prefix="/api/user",
    tags=["Auth"],
)


@user_router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_session)):
    user = await services.get_user_by_phone(db, data.phone)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(
        data={"sub": str(user.id)}, expiry=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = services.create_refresh_token(
        data={"sub": str(user.id)}, expiry=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


@user_router.post("/refresh", response_model=LoginResponse)
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_session)):
    try:
        user = await services.verify_refresh_token(db, data.refresh_token)
    except HTTPException:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(
        data={"sub": str(user.id)}, expiry=access_token_expires
    )

    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = services.create_refresh_token(
        data={"sub": str(user.id)}, expiry=refresh_token_expires
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


@user_router.get("/me", response_model=UserResponse)
async def me(user: models.User = Depends(services.get_current_user)):
    return user


@user_router.post("/token")
async def token(
    _: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    user = await services.get_user_by_phone(db, form_data.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(
        data={"sub": str(user.id)}, expiry=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = services.create_refresh_token(
        data={"sub": str(user.id)}, expiry=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


@user_router.post("/register", response_model=LoginResponse)
async def register(data: LoginRequest, db: AsyncSession = Depends(get_session)):
    user = await services.create_user(db, data.phone)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = services.create_access_token(
        data={"sub": str(user.id)}, expiry=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = services.create_refresh_token(
        data={"sub": str(user.id)}, expiry=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token}
