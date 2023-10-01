from bson import ObjectId

from fastapi import APIRouter, HTTPException

from lib.passwordfunc import hash_password,verify_password

from models.user import User 
from models.Book import Book

from database.users import users 
from database.books import books

from datetime import datetime, timedelta

import jwt

# from lib.passwordfunc import hash_password,verify_password

lib = APIRouter()

SECRET_KEY = "INDIGG"

ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=10)  # Token expiration time 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



#API FOR REGIATERING AN USER WITH THE DATABASE


@lib.post('/api/user')
def addUser(user : dict):
    if(user["password"] != user["cpassword"]):
        return {"message":"Password and confirm are not Matching"}
    
    userReg = {
        "email":user["email"],
        "password":hash_password(user["password"]),
        "cpassword":hash_password(user["cpassword"]),
        "name":user["name"],
        "createdAt": str(datetime.now())

    }
    result = users.insert_one(userReg)
    return {"message": "User added successfully", "user_id": str(result.inserted_id)}


#API TO GET DETAILS OF ALL USERS

@lib.get("/api/users")
async def getAllUsers():
    userslist = list(users.find())
    finalusers = [{**user, "_id": str(user["_id"])} for user in userslist]
    return finalusers

#API TO GET DETAILS OF AN SINGLE USER BASED ON _id

@lib.get("/api/user/{user_id}", response_model=User)
async def getParticularUserBasedOn_id(user_id: str):
    user = users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user["createdAt"] = str(user["createdAt"])

    user_model = User(**user)
    return user_model



#API TO LOGIN THE USER and if verified return an JWT Token expies in 10 Minutes after of Token generation


@lib.get("/api/auth/user")
def authUser(userData : dict):
    print(userData)
    userslist = list(users.find())
    finalusers = [{**user, "_id": str(user["_id"])} for user in userslist]
    print("-----------------")
    print(finalusers)
    for i in finalusers:
        print(i)
        print(type(i))
        if i["email"] == userData["email"]:
            if verify_password(userData["password"],i["password"]) == True:
                # all credentails are Ok
                #generating token 
                access_token = create_access_token({"sub": userData["email"]})
                return {"status" : "Login Successfull" , "token" : access_token , "expiresIn":"10 Minutes"}
            else:
                return {"status":"Login Failed due to Incorrect Password" ,"token" : None}
    return {"status":" Login Failed Email ID not Found"}

#-------------------------------------------------------------------------------------------------####################################



#APIS FOR HANDLING BOOKS BY THE LIBRARY ADMIN TO ADD BOOKS,UPDATE BOOKS,DELETE BOOKS,List all Books



@lib.post('/api/admin/addBooks')
def addUser(book : dict):
    bookReg = {
        "isbn":book["isbn"],
        "title":book["title"],
        "author":book["author"],
        "publishedYear":book["publishedYear"],
        "quantity":book["quantity"],
        "genre":book["genre"],
        "createdAt":str(datetime.now())

    }
    result = books.insert_one(bookReg)
    return {"message": "Book added successfully", "Book_id": str(result.inserted_id)}


@lib.get('/api/admin/getAllBooks')
def getAllBooks():
    bookslist = list(books.find())
    finalbooks = [{**book, "_id": str(book["_id"])} for book in bookslist]
    return {"status" : "Books Found" , "data" : finalbooks}



@lib.get('/api/admin/getBook/{book_isbn}')
def getSpecificBookDetailsonisbn(book_isbn : str):
    try:
        book = books.find_one({"isbn": book_isbn})
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        # book["createdAt"] = str(book["createdAt"])
        user_model = Book(**book)
        return {"status" : "Book Found" , "data" : user_model}
    except Exception as e :
        return {"status" : "Book Not Found"}
    



    
@lib.put('/api/admin/updateBookData/{isbn}')
def updateDatabasedOnIsbn(isbn : str, ubook: dict):
    try:
        print(isbn)
        existing_book = books.find_one({"isbn": isbn})
        if existing_book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        updated_data = ubook
        books.update_one({"isbn": isbn}, {"$set": updated_data})
        return {"status": "Book updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e
    

@lib.delete('/api/admin/deleteBook/{isbn}')
def deleteBookbasedOnIsbn(isbn:str):
    try:
        existing_book = books.find_one({"isbn": isbn})
        if existing_book is None:
            return {"status" : "Book Not Found"}

        books.delete_one({"isbn": isbn})

        return {"status": "Book deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e








