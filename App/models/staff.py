from .userLogin import UserLogin
from App.database import db

class Staff(UserLogin):

    reviews = db.relationship('Review',backref = db.backref('review',lazy = 'joined'))
    # List of reviews created??

    def __init__(self,id,username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.set_password(password)

    def toJSON(self):
        return{
            'staffid': self.id,
            'username': self.username,
            'email': self.email,
        }
