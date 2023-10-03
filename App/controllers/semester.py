from App.models import Semester
from App.database import db

# adds a new semester

def addSemester(semesterName,year,semStart,semEnd):
    newSemester = Semester(semesterName=semesterName,year=year,semStart=semStart,semEnd=semEnd)
    db.session.add(newSemester)
    db.session.commit()
    return newSemester