from App.models import Vote
from App.database import db

def addVote(voterId,reviewId,rating,upvote = None):
    newVote = Vote(voterId=voterId,reviewId=reviewId,rating=rating, upvote = upvote)
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
    votes = [vote.toJSON() for vote in votes]
    return votes

def getTotalScore(reviewId):
    votes = getVotesByReviewId(reviewId)
    sum = 0   
    for vote in votes:
        sum = sum + vote.rating
    return float(sum)

def getNumVotes(reviewId):
    votes = getVotesByReviewId(reviewId)
    return len(votes)

def calcAvgReviewScore(reviewId):
    score = getTotalScore(reviewId)
    voters = getNumVotes(reviewId)
    if voters == 0:
        return 0
    result = score/voters
    return (float(result))

def calcUpvotes(reviewId):
    votes = Vote.query.filter_by(reviewId = reviewId, upvote = True).all()
    return len(votes)

def calcDownvotes(reviewId):
    votes = Vote.query.filter_by(reviewId = reviewId, upvote = False).all()
    return len(votes)

def updateVote(voteId,rating,upvote):
    vote = getVote(voteId)
    if vote:
        vote.rating = rating
        vote.upvote = upvote
        db.session.add(vote)
        db.session.commit()
    return vote


#rejects ratings outside the range -3 to 3 as well as ratings equal to the review creator's rating
def validateDownvoteRating(c_rating,rating):
    if rating >= -3 and rating <=3:
        if  rating != c_rating:
            return True
    return False

def checkDuplicateVotes(reviewId,voterId):
    vote = Vote.query.filter_by(reviewId = reviewId, voterId = voterId).first()
    print(vote)
    if vote:
        return True
    
    return False