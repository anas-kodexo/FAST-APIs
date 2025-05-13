from app.auth.service import AuthService
from app.auth.utils import create_access_token, create_refresh_token
from datetime import timedelta


class AuthController:
    def __init__(self):
        self.service = AuthService()

    def register(self, db, user_data):
        return self.service.register_user(db, user_data)

    async def login(self, db, user_data):
        user = await self.service.authenticate_user(
            db, user_data.username, user_data.password
        )
        if not user:
            return None
        access_token = create_access_token(
            data={"sub": str(user.uid)}, expires_delta=timedelta(minutes=30)
        )
        refresh_token = create_refresh_token(
            {"sub": user["name"]}, expires_delta=timedelta(days=7)
        )
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "refresh_token": refresh_token,
        }

    async def refresh_access_token(self, db, refresh_token: str):
        return await self.service.refresh_access_token(refresh_token)
