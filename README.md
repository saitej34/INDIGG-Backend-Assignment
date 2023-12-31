# Book Management System - INDIGG ASSIGNMENT


Hey Hi I am Sai Teja.Y 

Resume Link : https://docs.google.com/document/d/1Tvqc-qmx2SL_e4guKVps4GP0GsCUZPzt/edit?usp=sharing&ouid=102640472593627877290&rtpof=true&sd=true

Let's explore all the APIs and their their request body formats and response formats, their name and and their endpoint names to which the call need to be made.

Get Access to this By ``` http://localhost:8000/docs ```

<img src="https://github.com/saitej34/INDIGG-Backend-Assignment/blob/main/APIS%20lIST.png" width="1000"/>


# Schema of Database 

<img src="https://github.com/saitej34/INDIGG-Backend-Assignment/blob/main/Schema.png" width="1000"/>

Steps to start the project : 

 - Clone the repository 
 - Install the following modules
 - fastapi,pydantic,pyjwt,pymongo,bcrypt
 - To run the app command follows : 
 ```sh
uvicorn main:app
```

`All the apis where {user_token} is necessary need to generate the token by logging the user will get get an JWT token valid to 300 Minutes  by calling 127.0.0.1:8000/api/auth/user with request body with email and password of user that you have registered with 127.0.0.1:8000/api/user`



# API to Register the user
```sh
127.0.0.1:8000/api/user
```
This api is used to register the user 

=> Hashed password gets stored into the Database

> Demo Request Body
{
    "email":"testemail1@gmail.com",
    "password":"testpassword",   
    "cpassword":"testpassword"
    "name":"testname",
    "createdAt": "2023-10-01T12:55:32.811+00:00",
    "borrowedBooks" : [],
    "booksHistory" : []
}

 >Demo Response by API
{
     "message": "User added successfully",
     "user_id": "6519cf5ddecb96d39ab20804"
} 

-------------------------------------------------------------------



## API to Login the user i.e to authenticate the user with email and password
 
 `Generates JWT Token upon successfull Login which can be valid upto some minutes which we can specify this in code access_token function  here i have specified 300 Minutes of time so therefore the token is valid only upto 300 Minutes ( 5 Hours )`
 
```sh
127.0.0.1:8000/api/auth/user
```

> Demo Request Body : 
{
    "email":"testemail1@gmail.com",
    "password":"testpassword"
}


> Demo Response :
{
  "status": "Login Successfull",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZW1haWxAZ21haWwuY29tIiwiZXhwIjoxNjk2MTkxMjA0fQ.NgVl9kZX09PM_nZ87Bvc4YJDlwJ14Iecw0j1jPx5r38",
  "expiresIn": "10 Minutes"
}


----------------------------------------------------


# API to Add Book to the Database
```sh
127.0.0.1:8000/api/admin/addBooks
```
This api is used to add Books to the Database

> Demo Request Body
{
        "isbn":"qwertyuiopkjhgfdsxcvbn",
        "title":"Book B",
        "author":"mani kandan",
        "publishedYear":2005,
        "quantity":"158",
        "genre":"Adventure Motivating"
}

 >Demo Response by API
{
  "message": "Book added successfully",
  "Book_id": "651a72468fde2b39a9adfe17"
}


----------------------------------------------------------------------------------------


# API TO GET ALL THE BOOKS DETAILS

```sh
http://127.0.0.1:8000/api/admin/getAllBooks
```
This api is used to add Books to the Database

> Demo Request Body
No Body Required

 > Demo Response by API
{
  "status": "Books Found",
  "data": [
    {
      "_id": "65193c71081d724bb33bb43d",
      "isbn": "qwertyj741242",
      "title": "Book of world",
      "author": "ertyuilkbvcvb",
      "publishedYear": 2003,
      "quantity": 200,
      "genre": "Engineering",
      "createdAt": "2023-10-01 15:01:29.719648"
    },
    {
      "_id": "651a72468fde2b39a9adfe17",
      "isbn": "qwertyuiopkjhgfdsxcvbn",
      "title": "Book A",
      "author": "saiteja",
      "publishedYear": 2005,
      "quantity": "150",
      "genre": "Adventure Motivasting",
      "createdAt": "2023-10-02 13:03:26.451419"
    }
  ]
}


# API TO GET SPECIFIC BOOK DETAILS 

```sh
http://127.0.0.1:8000/api/admin/getBook/{book_isbn}
```
book_isbn is ISBN of the  book

 > Demo Request : http://127.0.0.1:8000/api/admin/getBook/qwertyj741242

 > Demo Response
 {
  "status": "Book Found",
  "data": {
    "isbn": "qwertyj741242",
    "title": "Book of world",
    "author": "ertyuilkbvcvb",
    "publishedYear": 2003,
    "quantity": 200,
    "genre": "Engineering",
    "createdAt": "2023-10-01 15:01:29.719648"
  }
}


---------------------------------------------------------------------------------------------

# API TO UPDATE THE BOOK DATA BASED ON ISBN 

``` sh
http://127.0.0.1:8000/api/admin/updateBookData/{isbn}
```
 > Request demo url : 
Example :  I am trying to update the Name of Book 
 http://127.0.0.1:8000/api/admin/updateBookData/qwertyj741242
 Request Body : 
{
  "name":"Book of India"
}
Response :
{
  "status": "Book updated successfully"
}


-------------------------------------------------------------------------

# API TO DELETE A BOOK 

``` sh
http://127.0.0.1:8000/api/admin/deleteBook/{isbn}
```

 > Demo Request : 
 http://127.0.0.1:8000/api/admin/deleteBook/qwertyj741242
Response : 

{
  "status": "Book updated successfully"
}


--------------------------------------------------------

# API TO SEARCH FOR A BOOK BASED ON  title,author name,isbn number,genre

``` sh 
http://127.0.0.1:8000/api/books/search/{query}
```

 => query can be title/name of the book,author of the book,isbn of the book,genre of the book 
 => genre is an string with multiple genres as items in string called genre.
 Example : genre : "Adevnture Realistic Imaginary"

 > Request demo : http://127.0.0.1:8000/api/books/search/Adventure
 
 > Response : 
 {
  "status": "Books found",
  "data": [
    {
      "_id": "651a72468fde2b39a9adfe17",
      "isbn": "qwertyuiopkjhgfdsxcvbn",
      "title": "Book A",
      "author": "saiteja",
      "publishedYear": 2005,
      "quantity": "150",
      "genre": "Adventure Motivasting",
      "createdAt": "2023-10-02 13:03:26.451419"
    }
  ]
}

-------------------------------------------------

# API FOR USER TO BORROW THE BOOK FROM LIBRARY 

``` sh 
http://127.0.0.1:8000/api/borrow/{user_token}/{book_isbn}
```

This API is called when an user with id want to borrow the book from the library 

Here I have taken the days between borrow and return day be 20 Days i.e if the user borrows a book today he need to return in 20 days

 > Demo Request : http://127.0.0.1:8000/api/borrow/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZW1haWxAZ21haWwuY29tIiwiZXhwIjoxNjk2MjUzOTIwfQ.W2vHXx8NSNZnsK8AreF1_3t4bMmTska08BQpbx46Z1w/qwertyuiopkjhgfdsxcvbn
Demo Response : {"status" : "Transaction Successfull!!!   Borrow Successfull"}

--------------------------------------------------------------------------------

# API FOR USER TO RETURN THE BOOK FROM LIBRARY


``` sh 
http://127.0.0.1:8000/api/borrow/{user_token}/{book_isbn}
```

 > Demo Request : http://127.0.0.1:8000/api/return/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZW1haWxAZ21haWwuY29tIiwiZXhwIjoxNjk2MjUzOTIwfQ.W2vHXx8NSNZnsK8AreF1_3t4bMmTska08BQpbx46Z1w/qwertyuiopkjhgfdsxcvbn
 Demo Response : 
 {"status": "Transaction Successfull!!!  Book returned successfully"}
 
 
 ----------------------------------------------------------------------------
 
 
#  API TO GET RECOMMENDATIONS FOR A USER BASED ON HIS HISTORY 

In the schema we are storing the every book a user takes in his collection users as an array of booksHistory
from which we will get the genre,author the user is interested in taking and using this genre/author will recommend the the specific genre/author books to user.

``` sh 
http://127.0.0.1:8000/api/recommend/{user_token}
```


 > Demo Request : http://127.0.0.1:8000/api/recommend/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0ZW1haWxAZ21haWwuY29tIiwiZXhwIjoxNjk2MjUzOTIwfQ.W2vHXx8NSNZnsK8AreF1_3t4bMmTska08BQpbx46Z1w

----

 > Demo Response : We will get an array of books
 {
  "status": "Recommendation Successfull",
  "Books": [
    {
      "_id": "651b0cbeeeb42dee36b97f5c",
      "isbn": "978-0451167712",
      "title": "To Kill a Mockingbird",
      "author": "Harper Lee",
      "publishedYear": 1960,
      "quantity": 125,
      "genre": "Fiction",
      "createdAt": "2023-10-03 00:02:30.101986"
    },
    {
      "_id": "651b0cfbeeb42dee36b97f5e",
      "isbn": "978-0061120084",
      "title": "To Kill a Mockingbird",
      "author": "Harper Lee",
      "publishedYear": 2006,
      "quantity": 55,
      "genre": "Fiction",
      "createdAt": "2023-10-03 00:03:31.763220"
    },
    {
      "_id": "651b0d22eeb42dee36b97f5f",
      "isbn": "978-1400078776",
      "title": "The Kite Runner",
      "author": "Khaled Hosseini",
      "publishedYear": 2003,
      "quantity": 199,
      "genre": "Fiction",
      "createdAt": "2023-10-03 00:04:10.967504"
    },
    {
      "_id": "651b0dffeeb42dee36b97f61",
      "isbn": "978-0451524935",
      "title": "Pride and Prejudice",
      "author": "Jane Austen",
      "publishedYear": 1813,
      "quantity": 159,
      "genre": "Classic",
      "createdAt": "2023-10-03 00:07:51.539407"
    }
  ]
}
 

















