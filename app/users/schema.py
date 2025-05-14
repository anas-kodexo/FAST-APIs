from pydantic import BaseModel, EmailStr
import uuid
from typing import Optional


class UserOut(BaseModel):
    uid: uuid.UUID
    username: str
    email: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
