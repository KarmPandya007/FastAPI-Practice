from fastapi import FastAPI, Path, HTTPException, Query
# The Path() function is used to provide the metdata, validation rules and documentation hints for path parameters in your API endpoints. 
import json

app = FastAPI()

items = [
    {'id' : 1, "name" : "Karm"},
    {'id' : 2, "name" : "Ironman"},
    {'id' : 3, "name" : "MSD"},
]

def load_data() : 
    with open('patients.json', 'r') as f:
        data = json.load(f)
        return data

@app.get('/')
def hello() :
    return {"message" : "Hello World"}

@app.get('/health')
def health_check() :
    return {"status" : "Ok"}

@app.get('/items')
def get_items() :
    # return items
    return {"Items" : items}

@app.get('/patients')
def get_patients():
    data = load_data()
    return data

