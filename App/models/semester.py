from App.database import db


import enum
class SemNum (enum.Enum):
    SEM1 = "Semester 1"
    SEM2 = "Semester 2"
    SEM3 = "Summer"

class Semester(db.Model):
    semesterId = db.Column(db.Integer, primary_key=True)
    semesterName = db.Column(db.Enum(SemNum), nullable = False)
    year = db.Column(db.Integer)
    semStart = db.Column(db.Date, nullable = False)
    semEnd = db.Column(db.Date, nullable = False)

    def __init__(self,semesterName,year,semStart,semEnd):
            self.semesterName = semesterName
            self.year = year
            self.semStart = semStart
            self.semEnd = semEnd

    def __repr__(self):
        return f'<Semester {self.semesterId} {self.semesterName.value} {self.year}{self.semStart} {self.semEnd}>'

    def toJSON(self):
            return{
                'semesterId': self.semesterId,
                'semesterName': self.semesterName.value,
                'year': self.year,
                'semStart': self.semStart,
                'semEnd': self.semEnd
            }
    
