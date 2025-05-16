from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app.auth.utils import SECRET_KEY, ALGORITHM
from app.auth.models import User
from app.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    result = await db.execute(select(User).where(User.email == username))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Admin user not found"
        )

    return user


async def admin_only(
    current_user: User = Depends(get_current_user),
):
    print(f"Authenticated as: {current_user.username}, role: {current_user.role}")
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can perform this action",
        )

    return current_user
