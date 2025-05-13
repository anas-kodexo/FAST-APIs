from fastapi import APIRouter, Depends, HTTPException, status
from app.users.controllers import UserController
from app.auth.models import User
from app.users.schema import UserOut, UserUpdate
from app.db.main import get_session
from app.auth.dependencies import get_current_user
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


@user_router.put("/{username}")
async def update_user(
    username: str,
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return await user_controller.update_user(username, data, session)


@user_router.delete("/{username}")
async def delete_user(
    username: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    return await user_controller.delete_user(username, session)
