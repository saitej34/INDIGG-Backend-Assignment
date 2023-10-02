from pydantic import BaseModel 


class User(BaseModel):
    email:str
    password:str
    cpassword:str 
    name:str 
    genre:str
    createdAt:str
    borrowedBooks:list            #keeps track of books details and its date of borrow and date of return and I am considering return days timw will be of 20 Days from date of borrow
    booksHistory:list               #keeps track of books that the user has taken with only the isbns in tthe array and date