from App.models import Semester
from App.database import db
import datetime

# adds a new semester

def addSemester(semesterName,year,semStart,semEnd):
    try:
        newSemester = Semester(semesterName=semesterName,year=year,semStart=semStart,semEnd=semEnd)
        db.session.add(newSemester)
        db.session.commit()
        return newSemester
    
    except Exception:
        db.session.rollback()

def getSemester(semesterId):
    return Semester.query.filter_by(semesterId = semesterId).first()


def getAllSemesters(semesterId):
    return Semester.query.filter_by(semesterId = semesterId).all()


def assignSemester():

    current_date = datetime.date.today()
    current_semester = Semester.query.filter(Semester.semStart <= current_date, Semester.semEnd >= current_date).first()
    
    if current_semester:
        return current_semester.semesterId
    else:
        return None