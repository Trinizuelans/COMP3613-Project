from App.models import Staff
from App.database import db

# adds a new staff memeber

def addStaff (id,firstName,lastName,email,password):
    try:
        if get_staff(id) is None:
            newStaff = Staff(id = id,firstName = firstName,lastName = lastName,email = email, password = password)
            db.session.add(newStaff)
            db.session.commit()
            return newStaff
        return None
    
    except Exception:
        db.session.rollback()

# gets a staff memeber with specified id

def get_staff(id):
    return Staff.query.filter_by(id = id).first()

def get_staff_JSON(id):
    return Staff.query.filter_by(id = id).first().toJSON()

# gets all the staff memebers 

def get_all_staff():
     return Staff.query.all()

# gets all the staff memebers and jsonify it

def get_all_staff_json():
    staff = get_all_staff()
    if not staff:
        return []
    staff = [s.toJSON() for s in staff]
    return staff


    
