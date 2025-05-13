from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class UserRead(BaseModel):
    uid: UUID
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class RefreshTokenRequest(BaseModel):
    refresh_token: str
