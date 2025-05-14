from sqlmodel.ext.asyncio.session import AsyncSession
from app.auth.models import User
from sqlalchemy import select
from app.users.schema import UserOut, UserUpdate
from fastapi import HTTPException, status


class UserService:

    async def get_all_users(self, session: AsyncSession):
        statement = select(User).order_by(User.created_at)
        result = await session.exec(statement)
        print(f"User service reached")
        users = result.scalars().all()
        return [UserOut.from_orm(user) for user in users]

    async def get_user_by_name(self, username: str, session: AsyncSession):
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        user = result.scalars().first()
        if user:
            return UserOut.from_orm(user)
        return None

    async def delete_user_by_email(self, email: str, session: AsyncSession):
        user = await session.execute(select(User).filter_by(email=email)).scalar_one_or_none()

        print(f"Searching for user with email: {email}")
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email '{email}' not found.",
            )

        await session.delete(user)
        await session.commit()

        return {"detail": f"User with email '{email}' deleted successfully."}

    async def update_user_by_email(
        self, email: str, user_update: UserUpdate, session: AsyncSession
    ):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        user = result.scalars().first()
        if not user:
            return None

        if user_update.username is not None:
            user.username = user_update.username
        if user_update.email is not None:
            user.email = user_update.email

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return UserOut.from_orm(user)
