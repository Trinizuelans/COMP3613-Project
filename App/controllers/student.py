from App.models import Student,Faculty
from App.database import db
import App.controllers.review as review

# adds a new student 

def addStudent (id,firstName,lastName,email,year,programme,faculty):
    try:
        if get_student(id) is None:
            newStudent = Student(id = id,firstName = firstName,lastName = lastName,email = email,year = year,programme = programme,faculty = faculty)
            db.session.add(newStudent)
            db.session.commit()
            updateStudentStatistics(newStudent.id)
            return newStudent
        return None
    except Exception:
        db.session.rollback()


# gets a student with specified id

def get_student(id):
    return Student.query.filter_by(id = id).first()

# gets a student with specified id and jsonify it

def get_student_JSON(id):
    student = Student.query.filter_by(id = id).first()
    return student.toJSON()

# gets all the added students

def get_all_students():
     return Student.query.all()

# gets all the added students and jsonify it

def get_all_students_json():
    students = get_all_students()
    if not students:
        return []
    students = [student.toJSON() for student in students]
    return students

# updates year of a specified student 

def update_student_year(id, year):
    student = get_student(id)
    student.year = year
    
# updates programme of a specified student 

def update_student_programme(id, prog):
    student = get_student(id)
    student.programme = prog

 # updates all aspects of a specified student 

def update_student(id, firstname, lastname, email, year, prog,faculty):
    try:
        student = get_student(id)
        student.firstName = firstname
        student.lastName = lastname
        student.email = email
        student.year = year
        student.programme = prog
        student.faculty = format_faculty(faculty)
        print(student.faculty.value)

        db.session.add(student)
        db.session.commit()
        return student
    except Exception:
        db.session.rollback()


# gets the rated reviews of a specified student

def getRatedReviews(id):
    try:
        student = get_student(id)
        student.reviews = review.getReviewByStudent(student.id)
        db.session.add(student)
        db.session.commit()
        return student.reviews
    except Exception:
        db.session.rollback()

# calculates the karma of a specified student

def calcKarma(id):
     student = get_student(id)
     sum = 0
     length = len(student.reviews)

     if length == 0:
         return 0
     
     for rev in student.reviews:
        sum = sum + rev.score
     student.karma = sum/length
    
     return student.karma

# determines the standing of a specified student based on karma score

def determineStanding (id):
    student = get_student(id)

    if student.karma < -2:
        student.standing = "Poor"
    elif student.karma >= -2 and student.karma <-1:   
        student.standing = "Bad"    
    elif student.karma >= -1 and student.karma <1:   
        student.standing = "Normal"
    elif student.karma >= 1 and student.karma < 2:
        student.standing = "Good"
    else:
        student.standing = "Excellent"

    return student.standing

# updates the specfied student karma and standing after vote is casted 

def updateStudentStatistics(id):
    try:
        student = get_student(id)
        karma = calcKarma(id)
        standing = determineStanding(id)
        student.karma = karma
        student.standing = standing
        db.session.add(student)
        db.session.commit()
    except Exception:
        db.session.rollback()

def format_faculty(text):
    mappings = {
        "FST" : Faculty.FST,
        "FSS" : Faculty.FSS,
        "FFA" : Faculty.FFA,
        "FOL" : Faculty.FOL,
        "FMS" : Faculty.FMS,
        "FOE" : Faculty.FOE,
        "FHE" : Faculty.FHE,
        "FOS" : Faculty.FOS,
    }
    
    result = mappings.get(text, None)
    if result:
        return result
    return None
