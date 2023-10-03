from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

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
def get_users_action():
    users = get_all_staff_json()
    return jsonify(users)

@staff_views.route('/staff/login', methods=['POST'])
def staff_login_api():
  data = request.form
  token = jwt_authenticate(data['id'], data['password'])
  
  if not token:
    return jsonify(message='bad id or password given'), 401
  return jsonify(access_token=token)

@staff_views.route('/staff/signup', methods=['POST'])
def signup_action():
  try:
    data = request.form  # get data from form submission
    staff = addStaff(id = data['id'],firstName=data['firstName'],lastName=data['lastName'],email=data['email'],password=data['password'])
    
    if not staff:
        return jsonify(message='bad id or password given'), 401
    return jsonify(message="Staff account created!")

  except Exception:  # attempted to insert a duplicate user
    return jsonify(message='Staff account with id or email already exists!')














# @staff_views.route('/loginstaff', methods=['POST'])
# def login_action():
#     data = request.form
#     user = login(data['id'], data['password'])
#     if user:
#         login_user(user)
#         return 'Staff logged in!'
#     return 'bad id or password given', 401

# @staff_views.route('/logout', methods=['GET'])
# def logout_action():
#     data = request.form
#     user = login(data['id'], data['password'])
#     return 'Staff logged out!'
