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
    getReviewsByStudent_JSON,
    format_faculty

)

@student_views.route('/api/students', methods=['GET'])
@jwt_required()
def get_students_action():
    try:
        students =  get_all_students_json()
        return jsonify(students),200
    
    except Exception:
        return jsonify(error='Unable to retrieve students!'),400
    
@student_views.route('/student/<int:studentid>', methods=['GET'])
@jwt_required()
def search_student_action(studentid):
    try:
        student =  get_student(studentid)
        if not student:
            return jsonify(message='Unable to retrieve student!'),400
        
        student_json = get_student_JSON(studentid)
        return jsonify(student_json),200
    
    except Exception:
        return jsonify(error='Unable to retrieve student!'),400


@student_views.route('/student', methods=['POST'])
@jwt_required()
def create_student_action():
    try:
        data = request.form

        newStudent= addStudent(data['id'], data['firstname'], data['lastname'], data['email'], data['year'],data['programme'],data['faculty'])
        
        if newStudent is None:
            return jsonify(error='Invalid Id or email!'),401
        
        return jsonify(message='Student created!'),201
    except Exception: 
        return jsonify(error='Invalid Id or email!'),401
    
@student_views.route('/updatestudent', methods=['POST'])
@jwt_required()
def update_student_action():
    try:
        data = request.form
        student = update_student(data['id'], data['firstname'], data['lastname'], data['email'], data['year'],data['programme'],data['faculty'])
        if student is None:
            return jsonify(error='Unable to update Student!'),401
    
        return jsonify(message='Student updated!'),201
    
    except Exception: 
        return jsonify(error='Unable to update Student!'),401
    
@student_views.route('/student/<int:id>/review', methods=['GET'])
@jwt_required()
def student_review_action(id):
    try:
        reviews = getRatedReviews(id)
        return jsonify(getReviewsByStudent_JSON(id)),200

    except Exception: 
        return jsonify(error='Unable to get student reviews!'),400

