from App.database import db

class User(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(120),nullable = False, unique = True)

    def __init__(self,id, username, email):
        self.id = id
        self.username = username
        self.email = email

    def __repr__(self):
        return f'<User {self.id} {self.username}{self.email}>'
    
    def toJSON(self):
        return{
            'id': self.id,
            'username': self.username,
            'email' : self.email
        }