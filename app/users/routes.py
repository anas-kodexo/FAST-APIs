from fastapi import APIRouter, Depends, Body
from app.users.controllers import UserController
from app.auth.models import User
from app.users.schema import UserOut, UserUpdate
from app.db.main import get_session
from app.middlewares.auth_middleware import admin_only
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


@user_router.delete("/{email}")
async def delete_user_by_email(
    email: str,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(admin_only),
):
    print(f"del route hit")
    return await user_controller.delete_user_by_email(email, session)


@user_router.put("/{email}", response_model=UserOut)
async def update_user_by_email(
    email: str,
    user_update: UserUpdate = Body(...),
    session: AsyncSession = Depends(get_session),
    _: User = Depends(admin_only),
):
    return await user_controller.update_user_by_email(email, user_update, session)
