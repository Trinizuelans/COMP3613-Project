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

def getTotalScore(reviewId):
    votes = getVotesByReviewId(reviewId)
    sum = 0
    for vote in votes:
        sum = sum + vote.rating

    return sum

def getNumVotes(reviewId):
    votes = getVotesByReviewId(reviewId)
    return len(votes)

def calcAvgReviewScore(reviewId):
    score = getTotalScore(reviewId)
    voters = getNumVotes(reviewId)
    if voters == 0:
        return 0
    return (score/voters)

def calcUpvotes(reviewId):
    votes = Vote.query.filter_by(reviewId = reviewId, upvote = True).all()
    return len(votes)

def calcDownvotes(reviewId):
    votes = Vote.query.filter_by(reviewId = reviewId, upvote = False).all()
    return len(votes)

