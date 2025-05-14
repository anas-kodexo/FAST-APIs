from app.users.services import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from .schema import UserUpdate
from sqlmodel import select
from app.auth.models import User


class UserController:
    def __init__(self):
        self.service = UserService()

    async def get_all_users(self, session: AsyncSession):
        print("User controller reached")
        return await self.service.get_all_users(session)

    async def get_user_by_name(self, username: str, session: AsyncSession):
        user = await self.service.get_user_by_name(username, session)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with username '{username}' does not exist",
            )
        return user

    async def delete_user_by_email(self, email: str, db: AsyncSession):
        print(f"inside the del controller")
        return await self.service.delete_user_by_email(email, db)

    async def update_user_by_email(
        self, email: str, user_update: UserUpdate, session: AsyncSession
    ):
        updated_user = await self.service.update_user_by_email(
            email, user_update, session
        )
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email '{email}' does not exist",
            )
        return updated_user
