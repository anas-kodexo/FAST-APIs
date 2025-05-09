from fastapi import APIRouter, status, Depends , Response
from fastapi.exceptions import HTTPException
from src.books.schemas import Book_model, UpdateBookModel, BookCreateModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService

book_router = APIRouter()
book_service = BookService()


@book_router.get("/")
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session)
    return books


@book_router.post(
    "/create-book", status_code=status.HTTP_201_CREATED, response_model=Book_model
)
async def create_book(
    book_data: BookCreateModel, session: AsyncSession = Depends(get_session)
):
    new_book = await book_service.create_book(book_data, session)

    return new_book


@book_router.get("/book/{book_uid}" , response_model=Book_model)
async def get_book(book_uid: str, session: AsyncSession = Depends(get_session)) -> dict:

    book = await book_service.get_book(book_uid, session)

    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.patch("/book/{book_uid}")
async def update_book(
    book_uid: str,
    book_update_data: UpdateBookModel,
    session: AsyncSession = Depends(get_session),
) -> dict:

    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book:
        return updated_book

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.delete("/delete-book/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session)):

    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete is not True:
         print("the book has been deleted")
         return Response(status_code=204)  
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
