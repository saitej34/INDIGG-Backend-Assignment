from bson import ObjectId

from fastapi import APIRouter, HTTPException

from lib.passwordfunc import hash_password,verify_password

from models.user import User 
from models.Book import Book

from database.users import users 
from database.books import books

from datetime import datetime, timedelta

import jwt



lib = APIRouter()

SECRET_KEY = "INDIGG"

ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=100)  # Token expiration time 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"


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
        "createdAt": str(datetime.now()),
        "borrowedBooks" : [],
        "booksHistory" : []
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
    



## searching based on title,authorname,isbn number,genre etc



@lib.get('/api/books/search/{query}')               
def searchBooks(query: str):
    try:
        #regular expression case-insensitive search
        regex_query = {"$regex": query, "$options": "i"}
        matched_books = list(books.find({
            "$or": [
                {"title": regex_query},
                {"author": regex_query},
                {"isbn": regex_query},
                {"genre" : regex_query}
            ]
        }))
        if not matched_books:
            raise HTTPException(status_code=404, detail="No matching books found")
        for book in matched_books:
            book["_id"] = str(book["_id"])
        return {"status": "Books found", "data": matched_books}

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e





############## Borrow Return ########################## 



@lib.post('/api/borrow/{user_token}/{book_isbn}')
async def borrowBook(user_token: str, book_isbn: str):
    try:
        user_email = verify_token(user_token)
        emailf =  user_email["sub"] 
        user1 = users.find_one({"email": emailf})
        print("User",user1)
        book1 = books.find_one({"isbn": book_isbn})
        print("book",book1)
        if user1 is None:
            raise HTTPException(status_code=404, detail="User not found")
        if book1 is None:
            raise HTTPException(status_code=404, detail="Book not found")
        user1['_id'] = str(user1['_id'])
        book1['_id'] = str(book1['_id'])
        borrowedBooks = len(user1["borrowedBooks"])
        if(borrowedBooks >= 3):
            return {"status" : "Your Limit of 3 Books has been completed!!! You can borrow only 3 Books"}
        if book1["quantity"] > 0:
            await books.update_one({"isbn": book1["isbn"]}, {"$inc": {"quantity": -1}})
            book_details = {
                "isbn": book1["isbn"],
                "title": book1["title"],
                "author": book1["author"],
                "genre": book1["genre"],
                "borrowed_date": str(datetime.now()),
                "return_date": str(datetime.now() + timedelta(days=20))
            }
            user1["borrowedBooks"].append(book_details)
            user1["booksHistory"].append(book_details)
            await users.update_one({"email": user1["email"]}, {"$set": {"borrowedBooks": user1["borrowedBooks"],"booksHistory":user1["booksHistory"]}})
        else:
            raise HTTPException(status_code=400, detail="Book out of stock")
        
        return {"status" : "Transaction Successfull!!!   Borrow Successfull"}
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    


@lib.post('/api/return/{user_token}/{book_isbn}')
def returnBook(user_token: str, book_isbn: str):
    try:
        user_email = verify_token(user_token)
        emailf = user_email["sub"]
        user1 = users.find_one({"email": emailf})
        print("User", user1)
        book1 = books.find_one({"isbn": book_isbn})
        print("Book", book1)
        if user1 is None:
            raise HTTPException(status_code=404, detail="User not found")
        if book1 is None:
            raise HTTPException(status_code=404, detail="Book not found")
        
        user1['_id'] = str(user1['_id'])
        book1['_id'] = str(book1['_id'])

        index_to_remove = None
        for i, borrowed_book in enumerate(user1["borrowedBooks"]):
            if borrowed_book["isbn"] == book1["isbn"]:
                index_to_remove = i
                break
        
        if index_to_remove is not None:
            del user1["borrowedBooks"][index_to_remove]
            books.update_one({"isbn": book1["isbn"]}, {"$inc": {"quantity": 1}})
            users.update_one({"email": user1["email"]}, {"$set": {"borrowedBooks": user1["borrowedBooks"]}})
            return {"status": "Transaction Successfull!!!  Book returned successfully"}
        else:
            raise HTTPException(status_code=400, detail="You have not borrowed this book")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    



###################################        Book Recommendation               #################################### 




@lib.get('/api/recommend/{user_token}')
def getRecommendationBasedOnGenrendAuthor(user_token : str):
    user_email = verify_token(user_token)
    emailf = user_email["sub"]
    user1 = users.find_one({"email": emailf})
    user1['_id'] = str(user1['_id'])
    books = user1["booksHistory"]
    bookslist = list(books.find())
    finalbooks = [{**book, "_id": str(book["_id"])} for book in bookslist]
    genres=list()
    for book in books:
        print(type(book))
        genres.append(book["genre"])
    filtered_books = [book for book in finalbooks if book["genre"] in genres]
    if not filtered_books:
        return {"message": "No Recommendations Found"}
    return {"status" : "Recommendation Successfull" , "Books" : filtered_books}
    
        




