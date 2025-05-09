from fastapi import APIRouter , status , Depends
from fastapi.exceptions import HTTPException
from src.books.book_data import books
from src.books.schemas import Book_model, UpdateBookModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService

book_router = APIRouter()

@book_router.get("/")
async def get_all_books(session:AsyncSession = Depends(get_session)):
    return books

@book_router.post("/create-book", status_code=status.HTTP_201_CREATED )
async def create_book(book_data: Book_model):
    new_book = book_data.model_dump()
    books.append(new_book)
    
    return new_book


#getting book by id is performed in 2 ways:
@book_router.get("/book/{book_id}")
async def get_book(book_id:int) -> dict:       
    return books[book_id]

#2nd way:
@book_router.get("/book/{book_id}")
async def get_book(book_id:int) -> dict :
    for book in books:
        if book['id'] == book_id:
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail = "Book not found!")  


@book_router.patch("/book/{book_id}")
async def update_book(book_id:int , book_update_data:UpdateBookModel) -> dict:
    for book in books :
        if book["id"] == book_id:
            book["title"] = book_update_data.title
            book["author"] = book_update_data.author
            book["publisher"] = book_update_data.publisher
            book["pageCount"] = book_update_data.pageCount
            book["language"] = book_update_data.language
            
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Book not found")

@book_router.delete("/delete-book/{book_id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int):   
    for book in books :
        if book["id"] == book_id:
            books.remove(book)
            
            return{
    
            }        
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Book not found")

