def insert_patient_data(name, age):
    if type(name) == str and type(age) == int:
        print(name)
        print(age)
        print("Patient data inserted successfully")

insert_patient_data("John Doe", "30")