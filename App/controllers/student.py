from App.models import Student
from App.database import db

def addStudent (id,firstName,lastName,email,year,programme):
    newStudent = Student(id = id,firstName = firstName,lastName = lastName,email = email,year = year,programme = programme)
    db.session.add(newStudent)
    db.session.commit()
    return newStudent