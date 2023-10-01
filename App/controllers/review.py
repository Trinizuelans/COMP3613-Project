from App.models import Review
import App.controllers.vote as vote
from App.database import db

def addReview(creatorId,studentId,semesterId,comment,score):
    newReview = Review(creatorId=creatorId,studentId=studentId,semesterId=semesterId,comment=comment,score=0)
    db.session.add(newReview)
    db.session.commit()

    v = vote.addVote(creatorId,newReview.reviewId,score)
    newReview = addReviewVotes(newReview.reviewId)
    newReview.score = vote.calcAvgReviewScore(newReview.reviewId)
    db.session.add(newReview)
    db.session.commit()
  
    return newReview

def getReview(reviewId):
    return Review.query.filter_by(reviewId= reviewId).first()

def addReviewVotes(reviewId):
    votes = vote.getVotesByReviewId(reviewId)
    review = getReview(reviewId)
    if review:
        review.votes = votes
        db.session.add(review)
        db.session.commit()
        return review
    
def getAllReviews_JSON():
    reviews = Review.query.all()
    if not reviews:
        return []
    reviews = [review.toJSON()for review in reviews]
    return reviews

def updateReviewScore(reviewId):
    review  = getReview(reviewId)
    score = vote.calcAvgReviewScore(reviewId)
    review.score = score
    db.session.add(review)
    db.session.commit()