from sqlmodel.ext.asyncio.session import AsyncSession
from app.auth.models import User
from sqlalchemy import select
from app.users.schema import UserOut


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
