# Book Management System - INDIGG ASSIGNMENT

Let's explore all the APIs and their their request body formats and response formats, their name and and their endpoint names to which the call need to be made.

Steps to start the project : 

 - Clone the repository 
 - Install the following modules
 - fastapi,pydantic,pyjwt,pymongo,bcrypt
 - To run the app command follows : 
 ```sh
uvicorn main:app
```



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
 
 `Generates JWT Token upon successfull Login which can be valid upto some minutes which we can specify here i have specified 100 Minutes of time so therefore the token is valid only upto 100 Minutes`
 
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
















