from App.models import Review
import App.controllers.vote as vote
import App.controllers.student as stu
from App.database import db

# logs a review 

def addReview(creatorId,studentId,semesterId,comment,score):
    try:
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

    except Exception:
        db.session.rollback()


# gets first review matching the specified reviewID

def getReview(reviewId):
    return Review.query.filter_by(reviewId= reviewId).first()

# gets all the reviews matching the specified studentID

def getReviewByStudent(studId):
    return Review.query.filter_by(studentId= studId).all()

# gets all the reviews matching the specified studentID and jsonify it

def getReviewsByStudent_JSON(studId):
    reviews = Review.query.filter_by(studentId= studId).all()
    if not reviews:
        return []
    reviews = [review.toJSON()for review in reviews]
    return reviews
    
# gets all the reviews matching the specified creatorID  

def getReviewsByCreator(creatorId):
    return Review.query.filter_by(creatorId= creatorId).all()

# adds all the votes of a review, finds the review score, updates the number of upvotes, downvotes and votedifference

def addReviewVotes(reviewId):
    try:
        votes = vote.getVotesByReviewId(reviewId)
        review = getReview(reviewId)

        if review:
            review.votes = votes
            review.score = vote.calcAvgReviewScore(review.reviewId)
            upvote = vote.calcUpvotes(reviewId)
            downvote = vote.calcDownvotes(reviewId)
            votedifference = upvote - downvote

            review.upvote = upvote
            review.downvote = downvote
            review.votebalance = votedifference

            db.session.add(review)
            db.session.commit()

            stu.updateStudentStatistics(review.studentId)

            return review
        
    except Exception:
        db.session.rollback()

# gets all the reviews
    
def getAllReviews_JSON():
    reviews = Review.query.all()
    if not reviews:
        return []
    reviews = [review.toJSON()for review in reviews]
    return reviews

# gets all the reviews matching the specified creatorID and jsonify it 

def getAllCreatorReviews_JSON(creatorId):
    reviews = getReviewsByCreator(creatorId)
    if not reviews:
        return []
    reviews = [review.toJSON()for review in reviews]
    return reviews

# gets all the reviews matching the specified studentID and jsonify it

def getAllStudentReviews_JSON(studentId):
    reviews = getReviewByStudent(studentId)
    if not reviews:
        return []
    reviews = [review.toJSON()for review in reviews]
    return reviews

# updates the review score after another staff memeber casts a vote

def updateReviewScore(reviewId):
    try:
        review  = getReview(reviewId)
        score = vote.calcAvgReviewScore(reviewId)
        review.score = score
        db.session.add(review)
        db.session.commit()
    
    except Exception:
        db.session.rollback()


#checks existing upvotes and downvotes for double votes
def validateReviewVotes(reviewId,voterId):
    review = getReview(reviewId)

    for vote in review.votes:
        if vote.voterId == voterId:
            return False
        
    return True
