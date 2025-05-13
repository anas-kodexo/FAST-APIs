from sqlmodel.ext.asyncio.session import AsyncSession
from app.auth.models import User
from sqlalchemy import select
from app.users.schema import UserOut, UserUpdate
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError  

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

    async def delete_user_by_email(self, db: AsyncSession, email: str):
        try:
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            if not user:
                return False
            await db.delete(user)
            await db.commit()
            return True
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500, detail=f"Database error while deleting user: {str(e)}"
            )

    async def update_user_by_email(
        self, db: AsyncSession, email: str, user_update: UserUpdate
    ):
        try:
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            if not user:
                return False
            update_data = user_update.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(user, key, value)
            await db.commit()
            await db.refresh(user)
            return user
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Database error while updating user: {str(e)}"
            )
