from pydantic import BaseModel
from datetime import datetime , date
import uuid


class Book_model(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    publisherDate: date
    pageCount: int
    language: str
    created_at: datetime
    updated_at: datetime
    

class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    publisherDate: str
    pageCount: int
    language: str
 
class UpdateBookModel(BaseModel):
    title: str
    author: str
    publisher: str
    pageCount: int
    language: str
