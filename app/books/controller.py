from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import BookService
from .schemas import BookCreateModel, UpdateBookModel


class BookController:
    def __init__(self):
        self.service = BookService()

    async def get_all_books(self, session: AsyncSession):
        return await self.service.get_all_books(session)

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        return await self.service.create_book(book_data, session)

    async def get_book(self, book_uid: str, session: AsyncSession):
        book = await self.service.get_book(book_uid, session)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        return book

    async def update_book(self, book_uid: str, update_data: UpdateBookModel, session: AsyncSession):
        updated = await self.service.update_book(book_uid, update_data, session)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        return updated

    async def delete_book(self, book_uid: str, session: AsyncSession):
        success = await self.service.delete_book(book_uid, session)
        if not success:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        return JSONResponse(content={"message": f"Book with UID {book_uid} deleted successfully"})
