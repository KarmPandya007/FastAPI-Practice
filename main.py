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

@app.get('/patients/{patient_id}')
def get_patient_by_id(patient_id : str = Path(..., title="Th ID of the patient in the DB", example= 'P001')):
 # str because the tye of id in the patient.json is string
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    # return {"message" : "Patient not found"}
    raise HTTPException(status_code = 404, detail = "Patient not found")

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description = "Sort on the basis of height, weight or bmi"), 
                order : str = Query("asc", description = "Sort in asc or desc order")):

    valid_fields  = ["height", "weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code = 400, detail = f"Invalid field selected from {valid_fields}")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code = 400, detail = "Invalid order selection bw asc and desc")
    
    data = load_data()
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=(order == "desc"))
    return sorted_data



