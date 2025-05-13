from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from app.db.main import get_session
from app.auth.models import User
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

SECRET_KEY = "learning-fast-api"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def decode_jwt(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    payload = decode_jwt(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    session = await anext(get_session())
    result = await session.exec(select(User).where(User.uid == payload["sub"]))
    user = result.first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user
