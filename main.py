from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message" : "Hello World!"}


@app.get("/greet/{name}")
async def greet_name(name:str) -> dict :
    return {"message" : f"Hello {name}"}
    
#name not passed in the url will be treated as a query parameter    
@app.get("/greet")
async def greet_name(name:str) -> dict :
    return {"message" : f"Hello {name}"}
    

#query parameter + path parameter
@app.get("/new-greet/{name}")
async def greet_name(name:str, age:int) -> dict :
    return {"message" : f"Hello {name}" , "age": age}
    
    
#optional parameters   // optional gives a default value
@app.get("/optional-greet")
async def greet_name(name:Optional[str] = "User" , age:int =0 ) -> dict:
    return {"message" : f"Hello {name}" , "age": age} 

class BookCreateModel(BaseModel):
    title : str
    author: str
    

@app.post("/create-book")
async def create_book(book_data:BookCreateModel):
    return {
        "title" : book_data.title,
        "author" : book_data.author
    }
    

#using the fast api Header function to retrieve headers of a request.    
@app.get("/get-headers" , status_code= 500) #status codes can be set here despite of the actual code
async def get_headers(
    accept:str = Header(None),
    content_type:str =Header(None),
    user_agent: str = Header(None),
    host:str  = Header(None),
):
    request_headers = {}
    request_headers["Accept"] = accept
    request_headers["Content-Type"] = content_type,
    request_headers["User-agent"] = user_agent,
    request_headers["Host"] = host,
    
    return request_headers
    
    
    
    
    