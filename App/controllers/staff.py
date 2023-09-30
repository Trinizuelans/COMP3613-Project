from App.models import Staff
from App.database import db

def addStaff (id,firstName,lastName,email,password):
    newStaff = Staff(id = id,firstName = firstName,lastName = lastName,email = email, password = password)
    db.session.add(newStaff)
    db.session.commit()
    return newStaff