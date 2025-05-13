from app.users.services import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status


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
