from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from app.auth.models import User
from app.auth.utils import get_password_hash, verify_password
from app.auth.utils import create_access_token, verify_refresh_token
from datetime import timedelta
from fastapi import HTTPException, status


class AuthService:

    async def register_user(self, db: AsyncSession, user_data):

        existing_user = await db.execute(
            select(User).where(User.username == user_data.username)
        )
        existing_user = existing_user.scalars().first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Username '{user_data.username}' is already taken.",
            )

        existing_email = await db.execute(
            select(User).where(User.email == user_data.email)
        )
        existing_email = existing_email.scalars().first()

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email '{user_data.email}' is already registered.",
            )

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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token.",
            )

        try:
            # Create new access token using the payload
            new_access_token = create_access_token(
                {"sub": payload.get("sub")}, timedelta(minutes=30)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating new access token: {str(e)}",
            )

        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token,
        }
