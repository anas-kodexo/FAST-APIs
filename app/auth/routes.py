from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.controller import AuthController
from app.auth.schema import UserCreate, UserLogin, Token, UserRead, RefreshTokenRequest
from app.db.main import get_session

auth_router = APIRouter()
controller = AuthController()


@auth_router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_session)):
    return await controller.register(db, user)


@auth_router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_session)):
    token_data = await controller.login(db, user)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return Token(**token_data)


@auth_router.post("/refresh-token", response_model=Token)
async def refresh_token(
    data: RefreshTokenRequest, db: AsyncSession = Depends(get_session)
):

    token_data = await controller.refresh_access_token(db, data.refresh_token)

    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    return token_data
