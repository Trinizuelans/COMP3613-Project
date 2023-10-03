from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required


student_views = Blueprint('student_views', __name__, template_folder='../templates')


from App.controllers import (
    get_all_students,
    get_student,
    get_all_students_json, 
    addStudent,
    update_student,
    getRatedReviews,
    get_student_JSON,
    getReviewsByStudent_JSON

)

@student_views.route('/api/students', methods=['GET'])
def get_students_action():
    try:
        students =  get_all_students_json()
        return jsonify(students),200
    
    except Exception:
        return jsonify(message='Unable to retrieve students!'),400
    
@student_views.route('/student/<int:studentid>', methods=['GET'])
def search_student_action(studentid):
    try:
        student =  get_student(studentid)
        if not student:
            return jsonify(message='Unable to retrieve student!'),400
        
        student_json = get_student_JSON(studentid)
        return jsonify(student_json),200
    
    except Exception:
        return jsonify(message='Unable to retrieve student!'),400


@student_views.route('/student', methods=['POST'])
def create_student_action():
    try:
        data = request.form
        addStudent(data['id'], data['firstname'], data['lastname'], data['email'], data['year'],data['programme'])
        return jsonify(message='Student created!'),201
    except Exception: 
        return jsonify(message='Invalid Id or email!'),401
    
@student_views.route('/updatestudent', methods=['POST'])
def update_student_action():
    try:
        data = request.form
        update_student(data['id'], data['firstname'], data['lastname'], data['email'], data['year'],data['programme'])
        return jsonify(message='Student updated!'),201
    
    except Exception: 
        return jsonify(message='Unable to update Student!'),401
    
@student_views.route('/student/<int:id>/review', methods=['GET'])
def student_review_action(id):
    try:
        reviews = getRatedReviews(id)
        return jsonify(getReviewsByStudent_JSON(id)),200

    except Exception: 
        return jsonify(message='Unable to get student reviews!'),40

