from sqlmodel.ext.asyncio.session import AsyncSession
from app.auth.models import User
from sqlalchemy import select
from app.users.schema import UserOut, UserUpdate
from fastapi import HTTPException

class UserService:

    async def get_all_users(self, session: AsyncSession):
        statement = select(User).order_by(User.created_at)
        result = await session.exec(statement)
        print("User service reached")
        users = result.scalars().all()
        return [UserOut.from_orm(user) for user in users]

    async def get_user_by_name(self, username: str, session: AsyncSession):
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        user = result.scalars().first()
        if user:
            return UserOut.from_orm(user)
        return None

    async def update_user(self, username: str, data: UserUpdate, session: AsyncSession):
        from app.auth.models import User  # to avoid circular import

        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        user = result.first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def delete_user(self, username: str, session: AsyncSession):
        from app.auth.models import User

        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        user = result.first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await session.delete(user)
        await session.commit()
        return {"detail": f"User '{username}' deleted successfully"}
