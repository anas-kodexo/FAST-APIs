from pydantic import BaseModel
import uuid

class UserOut(BaseModel):
    uid: uuid.UUID
    username: str
    email: str

    class Config:
        from_attributes = True


