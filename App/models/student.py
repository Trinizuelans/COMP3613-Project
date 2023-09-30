from App.database import db
from .user import *
import enum

class Standing (enum.Enum):
    NEUTRAL = "Neutral"
    EXCELLENT = "Excellent"
    #need more categories for this

class Student (User):
    year = db.Column(db.Integer,primary_key = True)
    programme = db.Column(db.String(120), default = "NULL")
    reviews = db.relationship('Review',backref = db.backref('review',lazy = 'joined'))
    karma = db.Column(db.Numeric(precision=10, scale=2), default = 0)
    standing = db.Column(db.Enum(Standing), nullable = False, default = Standing.NEUTRAL)


    def __init__(self,id,username,email,year,programme):
        self.id = id
        self.username = username 
        self.email = email
        self.year = year
        self.programme = programme

    def __repr__(self):
        return f'<Student {self.id} {self.username} {self.email} {self.year} {self.programme}>'

    def toJSON(self):
        return{
            'studentId': self.id,
            'studentName': self.username,
            'email': self.email,
            'year': self.year,
            'programme': self.programme
        }