from pydantic import BaseModel 


class User(BaseModel):
    email:str
    password:str
    cpassword:str 
    name:str 
    genre:str
    createdAt:str