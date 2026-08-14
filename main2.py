from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/')
def hello():
    return {"message" : "Hello FastAPI Practice"}

@app.get('/users')
def get_users():
    return {"message" : "Get users endpoint"}

# Path Params
@app.get('/users/{user_id}')
def get_user(user_id : int):
    return {"id" : user_id}

# Query Params
@app.get("/users")
def get_users(name : str):
    return {"message" : name}

#  Default value query params 
@app.get("/products")
def get_products(limit: int = 10):
    return {"limit" : limit}
# By defualt the value will be 10, but if we do this : /products?limit=100000 it will return 100000

# Optional Query Params
@app.get("/users")
def get_users(name: str = None):
    return {"name" : name}
# If we do this : /users?name=John it will return John, otherwise it will return None (None is used for optional parameters)

@app.get('/items')
def get_items(name:str = None, price:int=0):
    return {"name" : name, 
            "price" : price
            }

# Example of query params: http://localhost:8000/items?name=John&price=100







# POST REQUEST : 


# @app.post('/create-user')
# def create_user(name:str, age:int):
#     return {
#         "name" : name,
#         "age" : age
#         }


# @app.post('/create-user')
# def create_user(user:dict):
#     return {
#         "message" : "User created successfully",
#         "data" : user
#         }

# Pydantic : Data Validation

class User(BaseModel):
    name:str
    age:int

@app.post('/create-user')
def create_user(user:User):
    return {
        "message" : "User created successfully",
        "data" : user
        }