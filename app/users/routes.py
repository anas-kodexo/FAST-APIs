from fastapi import APIRouter, Depends
from app.users.controllers import UserController
from app.users.schema import UserOut
from app.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

user_router = APIRouter()
user_controller = UserController()


@user_router.get("/", response_model=list[UserOut])
async def get_all_users(session: AsyncSession = Depends(get_session)):
    print("Route reached")
    return await user_controller.get_all_users(session)


@user_router.get("/{username}", response_model=UserOut)
async def get_user_by_name(username: str, session: AsyncSession = Depends(get_session)):
    print("Get user by name route reached")
    return await user_controller.get_user_by_name(username, session)
