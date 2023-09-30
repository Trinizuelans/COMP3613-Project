from App.models import Vote
from App.database import db

def addVote(voterId,reviewId,rating):
    newVote = Vote(voterId=voterId,reviewId=reviewId,rating=rating)
    db.session.add(newVote)
    db.session.commit()
    return newVote

def getVote(voteId):
    return Vote.query.filter_by(voteId = voteId).first()

def getVotesByReviewId(reviewId):
    return Vote.query.filter_by(reviewId = reviewId).all()
    
def getVotesByReviewId_JSON(reviewId): 
    votes = getVotesByReviewId(reviewId)
    if not votes:
        return []
    votes = [vote.get_json() for vote in votes]
    return votes

