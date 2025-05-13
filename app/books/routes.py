from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.main import get_session
from .schemas import Book_model, BookCreateModel, UpdateBookModel
from .controller import BookController

book_router = APIRouter()
controller = BookController()


@book_router.get("/", response_model=list[Book_model])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    return await controller.get_all_books(session)


@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book_model)
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session)):
    return await controller.create_book(book_data, session)


@book_router.get("/{book_uid}", response_model=Book_model)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    return await controller.get_book(book_uid, session)


@book_router.patch("/{book_uid}", response_model=Book_model)
async def update_book(book_uid: str, book_update_data: UpdateBookModel, session: AsyncSession = Depends(get_session)):
    return await controller.update_book(book_uid, book_update_data, session)


@book_router.delete("/{book_uid}")
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):
    return await controller.delete_book(book_uid, session)
