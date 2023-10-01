from App.models import Student
from App.database import db

def addStudent (id,firstName,lastName,email,year,programme):
    newStudent = Student(id = id,firstName = firstName,lastName = lastName,email = email,year = year,programme = programme)
    db.session.add(newStudent)
    db.session.commit()
    return newStudent

def get_student(id):
    return Student.query.filter_by(id = id).first()

def get_all_students():
     return Student.query.all()

def get_all_users_json():
    students = get_all_students()
    if not students:
        return []
    students = [student.get_json() for student in students]
    return students

def update_student_year(id, year):
    student = get_student(id)
    print(student.toJSON())
    student.year = year
    print(student.toJSON())

def update_student_programme(id, prog):
    student = get_student(id)
    print(student.toJSON())
    student.programme = prog
    print(student.toJSON())

# def calcKarma():