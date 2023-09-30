from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from App.database import db
from .user import User

class UserLogin(User, UserMixin):
    __abstract__ = True    
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, firstName,lastName, password):
        self.firstName = firstName
        self.lastName = lastName
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'firstName': self.firstName,
            'lastName': self.lastName
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)