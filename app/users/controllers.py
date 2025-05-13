from app.users.services import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from .schema import UserUpdate


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

    async def delete_user_by_email(self, db, email: str):
        try:
            success = await self.service.delete_user_by_email(db, email)
            if not success:
                raise HTTPException(
                    status_code=404, detail=f"User with email '{email}' not found"
                )
            return {"message": f"User with email '{email}' deleted successfully."}
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="An error occurred while deleting the user"
            )

    async def update_user_by_email(self, db, email: str, user_update: UserUpdate):
        try:
            user = await self.service.update_user_by_email(db, email, user_update)
            if not user:
                raise HTTPException(
                    status_code=404, detail=f"User with email '{email}' not found"
                )
            return user
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="An error occurred while updating the user"
            )
