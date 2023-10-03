from App.models import Student
from App.database import db
import App.controllers.review as review


def addStudent (id,firstName,lastName,email,year,programme):
    newStudent = Student(id = id,firstName = firstName,lastName = lastName,email = email,year = year,programme = programme)
    db.session.add(newStudent)
    db.session.commit()
    return newStudent

def get_student(id):
    return Student.query.filter_by(id = id).first()

def get_all_students():
     return Student.query.all()

def get_all_students_json():
    students = get_all_students()
    if not students:
        return []
    students = [student.toJSON() for student in students]
    return students

def update_student_year(id, year):
    student = get_student(id)
    # print(student.toJSON())
    student.year = year
    # print(student.toJSON())

def update_student_programme(id, prog):
    student = get_student(id)
    # print(student.toJSON())
    student.programme = prog
    # print(student.toJSON())

def update_student(id, firstname, lastname, email, year, prog):
    student = get_student(id)
    # print(student.toJSON())
    student.firstName = firstname
    student.lastName = lastname
    student.email = email
    student.year = year
    student.programme = prog
    db.session.add(student)
    db.session.commit()
    # print(student.toJSON())



def getRatedReviews(id):
    student = get_student(id)
    student.reviews = review.getReviewByStudent(student.id)
    print (student.reviews)
    return student.reviews

def calcKarma(id):
     student = get_student(id)
     sum = 0
     for rev in student.reviews:
        sum = sum + rev.score
     student.karma = sum/len(student.reviews)
     print(student)
     return student.karma

def determineStanding (id):
    student = get_student(id)
    if student.karma <= -1 :
      student.standing = "Disliked"
    if student.karma > -1 and student.karma < 1:
      student.standing = "Neutral"
    else:
      student.standing = "Liked"
    print(student)
    return student.standing