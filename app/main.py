import os
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel
import mysql.connector
app = FastAPI()
router = APIRouter(prefix="/api")
class Student(BaseModel):
 name: str
 course: str
def get_connection():
 return mysql.connector.connect(
 host=os.getenv("DB_HOST"),
 user=os.getenv("DB_USER"),
 password=os.getenv("DB_PASSWORD"),
 database=os.getenv("DB_NAME")
 )

@router.get("/health")
def health():
 return {
 "status": "UP"
 }
@router.get("/students")
def get_students():
 conn = get_connection()
 cursor = conn.cursor(dictionary=True)
 cursor.execute(
 "SELECT * FROM students"
 )
 result = cursor.fetchall()
 conn.close()
 return result

@router.get("/students/{student_id}")
def get_student(student_id: int):
 conn = get_connection()
 cursor = conn.cursor(dictionary=True)
 cursor.execute(
 "SELECT * FROM students WHERE id=%s",
 (student_id,)
 )
 result = cursor.fetchone()
 conn.close()
 return result

@router.post("/students")
def create_student(student: Student):
 conn = get_connection()
 cursor = conn.cursor()
 cursor.execute(
 """
 INSERT INTO students(name,course)
 VALUES(%s,%s)
 """,
 (
 student.name,
 student.course
 )
 )
 conn.commit()
 conn.close()
 return {
 "message": "Student Created"
 }

app.include_router(router)