#each element of the credits is a dictionnary 
#creds=[]
#each element, has the following keys : "Unit", "Coefficient(Total)", "Credit (Total)","Subjects" (each subject has its own coefficient and cred)
import json

creds = []

def add_unit():
    unit_name = input("Enter unit name: ")
    total_coefficient = float(input(f"Enter total coefficient for {unit_name}: "))
    total_credit = float(input(f"Enter total credit for {unit_name}: "))

    num_subjects = int(input(f"Enter the number of subjects for {unit_name}: "))
    subjects = []
    for _ in range(num_subjects):
        subject_name = input(f"Enter subject name: ")
        subject_coefficient = float(input(f"Enter coefficient for {subject_name}: "))
        subject_credit = float(input(f"Enter credit for {subject_name}: "))
        subjects.append({"Subject": subject_name, "Coefficient": subject_coefficient, "Credit": subject_credit})

    creds.append({
        "Unit": unit_name,
        "Coefficient(Total)": total_coefficient,
        "Credit(Total)": total_credit,
        "Subjects": subjects
    })

num_units = int(input("How many units to add? "))
for _ in range(num_units):
    add_unit()
print(json.dumps(creds, indent=4))
file_name=str(input("What do you want to call your JSON file ? "))

with open(f"{file_name}.json", 'w') as file:
    json.dump(creds, file, indent=4)
print("Filed saved successfully");

