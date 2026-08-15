from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel) : 
    id : int
    title : str
    isCompleted : bool

todos = []

@app.get('/todos')
def get_todos() : 
    return {
        "message" : "Fetched all the todos",
        "data" : todos
    }

@app.get('/todo/{todo_id}')
def get_todo(todo_id : int):
    for todo in todos:
        if todo.id == todo_id:
            return {
                "message" : "Todo found",
                "data" : todo
            }
    return {
        "message" : "Todo not found"
    }

@app.post('/create-todo')
def create_todo(todo : Todo) :
    todos.append(todo)
    return {
        "message" : "Todo created successfully",
        "data" : todo
    }

@app.put('/update-todo/{todo_id}')
def update_todo(todo_id: int, updated_todo: Todo):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index] = updated_todo
            return {
                "message": "Data Updated",
                "data": updated_todo
            }
    return {"error": "Todo not found"}

@app.delete('/delete-todos/{todo_id}')
def delete_todo(todo_id : int):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {
                "message" : "Todo deleted successfully",
                "data" : todo
            }
    return {"error": "Todo not found"}