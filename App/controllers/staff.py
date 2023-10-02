from App.models import Staff
from App.database import db

def addStaff (id,firstName,lastName,email,password):
    newStaff = Staff(id = id,firstName = firstName,lastName = lastName,email = email, password = password)
    db.session.add(newStaff)
    db.session.commit()
    return newStaff

def get_staff(id):
    return Staff.query.filter_by(id = id).first()

def get_all_staff():
     return Staff.query.all()

def get_all_staff_json():
    staff = get_all_staff()
    if not staff:
        return []
    staff = [s.toJSON() for s in staff]
    return staff


    
