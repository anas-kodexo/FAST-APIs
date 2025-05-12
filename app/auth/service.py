from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.auth.models import User
from app.auth.utils import get_password_hash, verify_password


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
