from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector

# MySQL Database Configuration
db_config = {
    'user': 'username',
    'password': 'password',
    'host': 'localhost',
    'database': 'Educational_Database'
}

# FastAPI App
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"],  # Update this with your frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Database Connection
db_connection = mysql.connector.connect(**db_config)
db_cursor = db_connection.cursor()

# Pydantic Model for Student
class Student(BaseModel):
    Student_Id: int
    First_name: str
    Middle_name: str
    Last_name: str
    Date_of_Birth: str
    Class_year: int
    Phone_number: str

class Professor(BaseModel):
    Professor_Id: int
    First_name: str
    Middle_name: str
    Last_name: str
    Date_of_Birth: str
    Phone_number: str

# Routes
@app.post("/students/")
async def create_student(student: Student):
    query = "INSERT INTO Students (Student_Id, First_name, Middle_name, Last_name, Date_of_Birth, Class_year, Phone_number)"
    query += " VALUES (%s, %s, %s, %s, %s, %s, %s)"
    print(student)
    values = (student.Student_Id, student.First_name, student.Middle_name, student.Last_name, student.Date_of_Birth, student.Class_year, student.Phone_number)
    db_cursor.execute(query, values)
    db_connection.commit()
    print(student)

@app.get("/students/")
async def get_students():
    query = "SELECT Student_Id, First_name, Middle_name, Last_name, Date_of_Birth, Class_year, Phone_number FROM Students"
    db_cursor.execute(query)
    students = []
    for result in db_cursor.fetchall():
        students.append({
            "Student_Id": result[0],
            "First_name": result[1],
            "Middle_name": result[2],
            "Last_name": result[3],
            "Date_of_Birth": result[4],
            "Class_year": result[5],
            "Phone_number": result[6]
        })
    return students

# Close database connection when the application finishes executing
@app.on_event("shutdown")
async def shutdown_event():
    db_cursor.close()
    db_connection.close()

# Run the application
if __name__ == "__main__":
    import uvicorn
    if db_connection.is_connected():
        print("Connected to MySQL database")
    else:
        print("Failed to connect to MySQL database")
    uvicorn.run(app, host="0.0.0.0", port=8000)
