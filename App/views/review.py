from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required

from App.controllers import(addReview)

review_views = Blueprint('review_views', __name__, template_folder='../templates')

@review_views.route('/review', methods=['POST'])
@jwt_required()
def create_review_action():
    try:
        data = request.form
        review = addReview(data['id'],data['studentId'],data['semesterId'],data['comment'],data['score'])
        if not review:
            return jsonify(error='Review was unable to be created!'), 401
        return jsonify(message='Review created!'), 201
    except Exception:
        return jsonify(error='Review was unable to be created!'), 401
    
