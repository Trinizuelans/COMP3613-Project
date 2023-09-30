from flask_login import login_user, login_manager, logout_user, LoginManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

from App.models import Staff

def jwt_authenticate(id, password):
  staff = Staff.query.filter_by(id= id).first()
  if staff and staff.check_password(password):
    return create_access_token(identity=id)
  return None

def login(id, password):
    staff = Staff.query.filter_by(id=id).first()
    if staff and staff.check_password(password):
        return staff
    return None

def setup_flask_login(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return Staff.query.get(user_id)
    
    return login_manager

def setup_jwt(app):
    jwt = JWTManager(app)

    @jwt.user_identity_loader
    def user_identity_lookup(identity):
        user = Staff.query.filter_by(id=identity).one_or_none()
        if user:
            return user.id
        return None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return Staff.query.get(identity)

    return jwt