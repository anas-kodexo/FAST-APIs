from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.controller import AuthController
from app.auth.schema import UserCreate, UserLogin, Token, UserRead
from app.db.main import get_session

auth_router = APIRouter()
controller = AuthController()


@auth_router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_session)):
    return await controller.register(db, user)


@auth_router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_session)):
    token = await controller.login(db, user)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token
