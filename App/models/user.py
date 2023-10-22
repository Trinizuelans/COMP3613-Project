from App.database import db

class User(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    firstName =  db.Column(db.String(120), nullable=False)
    lastName = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120),nullable = False, unique = True)
    profile_picture = db.Column(db.String, nullable = False, default = "images/default-profile-picture.jpg")


    # def __init__(self,id, firstName,lastName, email):
    #     self.id = id
    #     self.firstName = firstName
    #     self.lastName = lastName
    #     self.email = email

    def __repr__(self):
        return f'<User {self.id} {self.firstName} {self.lastName} {self.email}{self.profile_picture}>'
    
    def toJSON(self):
        return{
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email' : self.email,
            'profile_picture' : self.profile_picture
        }