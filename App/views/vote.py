from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from App.controllers import getReview,addVote,addReviewVotes,validateReviewVotes,validateDownvoteRating,checkDuplicateVotes
vote_views = Blueprint('vote_views', __name__, template_folder='../templates')



@vote_views.route('/upvote', methods=['POST'])
@jwt_required()
def create_upvote_action():
    
    try:
        data = request.form
        reviewId = data['reviewId']
        voterId = data['voterId']
        review = getReview(reviewId)
        rating = review.votes[0].rating
        if checkDuplicateVotes(reviewId,voterId):
            return jsonify(error='Staff cannot vote twice!'),401

        vote = addVote(data['voterId'],data['reviewId'],rating,upvote=True)
        print(addVote)
        review = addReviewVotes(reviewId)
        return jsonify(message='Upvote Successful!'), 201
    
    except Exception:
        return jsonify(error='Upvote Unsuccessful!'), 401
    

@vote_views.route('/downvote', methods=['POST'])
@jwt_required()
def create_downvote_action():
    try:
        data = request.form
        reviewId = data['reviewId']
        voterId = data['voterId']
        rating = int(data['rating'])

        if checkDuplicateVotes(reviewId,voterId):
            return jsonify(error='Staff cannot vote twice!'),402

        review = getReview(reviewId)
        c_rating = review.votes[0].rating
        print(c_rating)
        v = validateDownvoteRating(c_rating,rating)

        if v == False:
           return jsonify(error='Rating out of range or equal to review creator rating'), 401
        
        else: 
           vote = addVote(voterId,reviewId,rating,upvote=False)
           review = addReviewVotes(reviewId)
           return jsonify(message='Downvote Successful!'), 200
        
    
    except Exception:
        return jsonify(error=' Downvote Unsuccessful!'), 401