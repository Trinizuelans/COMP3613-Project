from App.models import Vote
from App.database import db

# adds a vote to a specific review 

def addVote(voterId,reviewId,rating,upvote = None):
    newVote = Vote(voterId=voterId,reviewId=reviewId,rating=rating, upvote = upvote)
    db.session.add(newVote)
    db.session.commit()
    return newVote

# gets a specifc vote 

def getVote(voteId):
    return Vote.query.filter_by(voteId = voteId).first()

# gets all the votes for a specific review 

def getVotesByReviewId(reviewId):
    return Vote.query.filter_by(reviewId = reviewId).all()

# gets all the votes for a specific review and jsonify it
    
def getVotesByReviewId_JSON(reviewId): 
    votes = getVotesByReviewId(reviewId)
    if not votes:
        return []
    votes = [vote.toJSON() for vote in votes]
    return votes

# calculates the total score of a specific review

def getTotalScore(reviewId):
    votes = getVotesByReviewId(reviewId)
    sum = 0   
    for vote in votes:
        sum = sum + vote.rating
    return float(sum)

# gets number of votes for a specifc review

def getNumVotes(reviewId):
    votes = getVotesByReviewId(reviewId)
    return len(votes)

# calculates the average score for a specific review

def calcAvgReviewScore(reviewId):
    score = getTotalScore(reviewId)
    voters = getNumVotes(reviewId)
    if voters == 0:
        return 0
    result = score/voters
    return (float(result))

# calculates the number of upvotes for a specifc review

def calcUpvotes(reviewId):
    votes = Vote.query.filter_by(reviewId = reviewId, upvote = True).all()
    return len(votes)

# calculates the number of downvotes for a specifc review

def calcDownvotes(reviewId):
    votes = Vote.query.filter_by(reviewId = reviewId, upvote = False).all()
    return len(votes)

# updates a rating of a specific vote

def updateVote(voteId,rating,upvote):
    vote = getVote(voteId)
    if vote:
        vote.rating = rating
        vote.upvote = upvote
        db.session.add(vote)
        db.session.commit()
    return vote

# checks wether rating is within range ie -3 to 3 and ensure it's not equal to the creator's rating

def validateDownvoteRating(c_rating,rating):
    if rating >= -3 and rating <=3:
        if  rating != c_rating:
            return True
    return False

# checks to see if there already exist a vote for a specific voter in a specifc review 

def checkDuplicateVotes(reviewId,voterId):
    vote = Vote.query.filter_by(reviewId = reviewId, voterId = voterId).first()
    print(vote)
    if vote:
        return True
    
    return False