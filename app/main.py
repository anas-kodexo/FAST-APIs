from fastapi import FastAPI
from app.books.routes import book_router
from contextlib import asynccontextmanager
from app.db.main import init_db
from app.auth.routes import auth_router


@asynccontextmanager
async def life_span(app: FastAPI):
    print(f"Server is starting..")
    await init_db()
    yield
    print(f"Server has stopped")


version = "v1"
app = FastAPI(
    title="Bookly",
    description="A REST API for a book review service",
    version=version,
    lifespan=life_span,
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["Auth"])


