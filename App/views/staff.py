from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from App.database import db

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate, 
    get_all_users,
    get_all_users_json,
    jwt_required,
    login,
    login_user,
    get_all_staff_json,
    addStaff
)


staff_views = Blueprint('staff_views', __name__, template_folder='../templates')


@staff_views.route('/api/staff', methods=['GET'])
@jwt_required()
def get_staff_action():
    try:
      users = get_all_staff_json()
      return jsonify(users)
    except Exception:
       return jsonify(error='Unable to retrieve staff!'),401

@staff_views.route('/api/login', methods=['POST'])
def staff_login_api():
  data = request.form
  token = jwt_authenticate(data['id'], data['password'])
  
  if not token:
    return jsonify(error='bad id or password given'), 401
  return jsonify(access_token=token)

@staff_views.route('/staff/signup', methods=['POST'])
def signup_action():
  try:
    data = request.form  # get data from form submission
    staff = addStaff(id = data['id'],firstName=data['firstName'],lastName=data['lastName'],email=data['email'],password=data['password'])
    
    if not staff:
        return jsonify(error='bad id or password given'), 401
    return jsonify(message="Staff account created!")

  except Exception:  # attempted to insert a duplicate user
    return jsonify(error='Staff account with id or email already exists!')

@staff_views.route('/staff/login', methods=['POST'])
def login_action():
    data = request.form
    user = login(data['id'], data['password'])
    if user:
        login_user(user)
        return jsonify(message = 'Staff logged in!') ,200
    return jsonify(error ='bad id or password given'), 401

@staff_views.route('/logout', methods=['GET'])
def logout_action():
    try:
      data = request.form
      user = login(data['id'], data['password'])
      return jsonify(message = 'Staff logged out!') ,200
    except Exception:
       return jsonify(error = 'Unable to log out!') ,401
