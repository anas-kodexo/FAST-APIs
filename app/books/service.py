# app/books/service.py
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from .models import Book_model
from .schemas import BookCreateModel, UpdateBookModel


class BookService:
    async def get_all_books(self, session: AsyncSession):
        stmt = select(Book_model).order_by(desc(Book_model.created_at))
        result = await session.exec(stmt)
        return result.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        stmt = select(Book_model).where(Book_model.uid == book_uid)
        result = await session.exec(stmt)
        return result.first()

    async def create_book(self, book_data: BookCreateModel, session: AsyncSession):
        new_book = Book_model(**book_data.model_dump())
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book

    async def update_book(self, book_uid: str, update_data: UpdateBookModel, session: AsyncSession):
        book = await self.get_book(book_uid, session)
        if book:
            for k, v in update_data.model_dump(exclude_unset=True).items():
                setattr(book, k, v)
            await session.commit()
            await session.refresh(book)
            return book
        return None

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book = await self.get_book(book_uid, session)
        if book:
            await session.delete(book)
            await session.commit()
            return True
        return False
