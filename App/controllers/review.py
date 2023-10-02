from App.models import Review
import App.controllers.vote as vote
from App.database import db

def addReview(creatorId,studentId,semesterId,comment,score):

    #create a new review and commit it to generate a review ID

    newReview = Review(creatorId=creatorId,studentId=studentId,semesterId=semesterId,comment=comment,score=0)
    db.session.add(newReview) 
    db.session.commit()

    #create a vote for the creator of the review i.e rating from -3 to 3

    v = vote.addVote(creatorId,newReview.reviewId,score)

    #take the vote of the creator of the review and assign it to 0 postion of the votes [] in review

    newReview = addReviewVotes(newReview.reviewId)

    #calculates score of the review after, NB: Only the 1 vote is present atm which is creator vote

    newReview.score = vote.calcAvgReviewScore(newReview.reviewId)

    db.session.add(newReview)
    db.session.commit()
  
    return newReview

def getReview(reviewId):
    return Review.query.filter_by(reviewId= reviewId).first()

def getReviewByStudent(studId):
    return Review.query.filter_by(studentId= studId).all()

def getReviewsByCreator(creatorId):
    return Review.query.filter_by(creatorId= creatorId).all()

def addReviewVotes(reviewId):
    votes = vote.getVotesByReviewId(reviewId)
    review = getReview(reviewId)
    if review:
        review.votes = votes
        review.score = vote.calcAvgReviewScore(review.reviewId)
        db.session.add(review)
        db.session.commit()
        return review
    
def getAllReviews_JSON():
    reviews = Review.query.all()
    if not reviews:
        return []
    reviews = [review.toJSON()for review in reviews]
    return reviews

def getAllCreatorReviews_JSON(creatorId):
    reviews = getReviewsByCreator(creatorId)
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