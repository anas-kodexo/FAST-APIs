from app.auth.service import AuthService
from app.auth.utils import create_access_token, create_refresh_token, verify_password
from datetime import timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.auth.models import User
from fastapi import HTTPException, status


class AuthController:
    def __init__(self):
        self.service = AuthService()

    def register(self, db, user_data):
        return self.service.register_user(db, user_data)

    # auth/service.py

    async def authenticate_user(self, db: AsyncSession, username: str, password: str):
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalars().first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with username '{username}' does not exist.",
            )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password.",
            )

        return user

    async def refresh_access_token(self, db, refresh_token: str):
        return await self.service.refresh_access_token(refresh_token)
