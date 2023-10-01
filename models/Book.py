from pydantic import BaseModel 

class Book(BaseModel):
    isbn:str
    title:str 
    author:str
    publishedYear:int
    quantity:int 
    genre:str
    createdAt:str
