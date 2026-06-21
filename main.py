from fastapi import FastAPI

app = FastAPI()

items = [
    {'id' : 1, "name" : "Karm"},
    {'id' : 2, "name" : "Ironman"},
    {'id' : 3, "name" : "MSD"},
]

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

@app.get('/items/{item_id}')
def get_item(item_id : int) :
    for item in items :
        if item["id"] == item_id :
            return item
    return {"message" : "Item not found"}

@app.get('/items/names')
def get_items_names():
    return [item["name"] for item in items]