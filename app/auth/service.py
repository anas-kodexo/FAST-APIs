from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.auth.models import User
from app.auth.utils import get_password_hash, verify_password
from app.auth.utils import create_access_token, verify_refresh_token
from datetime import timedelta


class AuthService:
    async def register_user(self, db: AsyncSession, user_data):
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def authenticate_user(self, db: AsyncSession, username: str, password: str):
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        if not user or not verify_password(password, user.hashed_password):
            return None

        user_dict = {
            "uid": user.uid,
            "email": user.email,
            "name": user.username,
        }

        user_dict.pop("hashed_password", None)
        return user_dict

    async def refresh_access_token(self, refresh_token: str):

        payload = verify_refresh_token(refresh_token)
        if not payload:
            return None

        new_access_token = create_access_token(
            {"sub": payload.get("sub")}, timedelta(minutes=30)
        )
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token,
        }
