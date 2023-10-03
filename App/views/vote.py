from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import current_user, login_required
from App.controllers import getReview,addVote,addReviewVotes,validateReviewVotes,validateDownvoteRating
vote_views = Blueprint('vote_views', __name__, template_folder='../templates')



@vote_views.route('/upvote', methods=['POST'])
def create_upvote_action():
    try:
        data = request.form
        reviewId = data['reviewId']
        voterId = data['voterId']
        review = getReview(reviewId)
        print(review)
        rating = review.votes[0].rating
        print(rating)
        if not validateReviewVotes(reviewId,voterId):
            return jsonify(message='Error: Staff cannot vote twice!'),402

        vote = addVote(data['voterId'],data['reviewId'],rating,True)
        print(addVote)
        review = addReviewVotes(reviewId)
        return jsonify(message='Upvote Successful!'), 200
    
    except Exception:
        return jsonify(message='Error: Upvote Unsuccessful!'), 401
    

@vote_views.route('/downvote', methods=['POST'])
def create_downvote_action():
    try:
        data = request.form
        reviewId = data['reviewId']
        voterId = data['voterId']
        rating = data['rating']

        review = getReview(reviewId)
        # c_rating = review.votes[0].rating
        # v = validateDownvoteRating(c_rating,rating)
        
        # print("v"+str(v))

        # if not validateReviewVotes(reviewId,voterId):
        #     return jsonify(message='Error: Staff cannot vote twice!'),402
        
        # if validateDownvoteRating(review,rating):
        vote = addVote(voterId,reviewId,rating,False)
        review = addReviewVotes(reviewId)
        return jsonify(message='Downvote Successful!'), 200
        # return jsonify(message='Rating out of range or equal to review creator rating'), 401
    
    except Exception:
        return jsonify(message='Error: Downvote Unsuccessful!'), 401