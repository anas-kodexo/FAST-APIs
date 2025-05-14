from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from app.auth.controller import AuthController
from app.auth.schema import UserCreate, UserLogin, Token, UserRead, RefreshTokenRequest
from app.db.main import get_session
from .utils import create_access_token, create_refresh_token

auth_router = APIRouter()
controller = AuthController()


@auth_router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_session)):
    return await controller.register(db, user)


@auth_router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_session)):
    user_obj = await controller.authenticate_user(db, user.username, user.password)

    access_token = create_access_token({"sub": user_obj.email, "role": user_obj.role})
    refresh_token = create_refresh_token({"sub": user_obj.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@auth_router.post("/refresh-token", response_model=Token)
async def refresh_token(
    data: RefreshTokenRequest, db: AsyncSession = Depends(get_session)
):

    token_data = await controller.refresh_access_token(db, data.refresh_token)

    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    return token_data
