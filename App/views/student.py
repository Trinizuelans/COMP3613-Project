from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required


student_views = Blueprint('student_views', __name__, template_folder='../templates')


from App.controllers import (
    get_all_students,
    get_all_students_json,   
)

@student_views.route('/api/students', methods=['GET'])
def get_student_action():
    students =  get_all_students_json()
    return jsonify(students)