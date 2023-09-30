from .userLogin import UserLogin
from App.database import db

class Staff(UserLogin):

    reviews = db.relationship('Review',backref = db.backref('review',lazy = 'joined'))
    # List of reviews created??

    def __init__(self,id,firstName,lastName, email, password):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.reviews = []
        self.set_password(password)

    def __repr__(self):
        return f'<Staff {self.id} {self.firstName} {self.lastName} {self.email} {self.reviews}>'

    def toJSON(self):
        return{
            'staffid': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'reviews': self.reviews
        }
