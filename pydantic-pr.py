from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# class User(BaseModel) : 
#     name : str 
#     age : int
#     email : str

# @app.post('/create-user')
# def create_user(user: User) : 
#     return {
#         "message" : "User created successfully", 
#         "data" : user
#     }



# Nested Modules : 

class Address(BaseModel) : 
    city : str 
    pin_code : int

class User(BaseModel) : 
    name : str 
    age : int
    email : str
    address : Address 

@app.post('/create-user')
def create_user(user: User) : 
    return {
        "message" : "User created successfully", 
        "data" : user
    }