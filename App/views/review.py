from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from App.controllers import(addReview)

review_views = Blueprint('review_views', __name__, template_folder='../templates')

@review_views.route('/logreview', methods=['POST'])
def create_student_action():
    data = request.form
    review = addReview(data['id'],data['studentId'],data['semesterId'],data['comment'],data['score'])
    return jsonify(message='success'), 200