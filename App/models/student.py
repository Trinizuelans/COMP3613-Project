from App.database import db
from .user import *
import enum

class Standing (enum.Enum):
    NEUTRAL = "Neutral"
    EXCELLENT = "Excellent"
    #need more categories for this

class Student (User):
    year = db.Column(db.Integer)
    programme = db.Column(db.String(120), default = "NULL")
    reviews = db.relationship('Review',backref = db.backref('student',lazy = 'joined'))
    karma = db.Column(db.Numeric(precision=10, scale=2), default = 0)
    standing = db.Column(db.Enum(Standing), nullable = False, default = Standing.NEUTRAL)


    def __init__(self,id,firstName,lastName,email,year,programme):
        self.id = id
        self.firstName = firstName 
        self.lastName = lastName
        self.email = email
        self.year = year
        self.programme = programme

    def __repr__(self):
        return f'<Student {self.id} {self.firstName} {self.lastName} {self.email} {self.year} {self.programme}>'

    def toJSON(self):
        return{
            'studentId': self.id,
            'firstName': self.firstName,
            'lastName':self.lastName,
            'email': self.email,
            'year': self.year,
            'programme': self.programme
        }