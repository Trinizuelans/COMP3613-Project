from App.database import db

class Vote (db.Model):
    voteId = db.Column(db.Integer, primary_key=True)
    voterId =  db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    reviewId = db.Column(db.Integer, db.ForeignKey('review.reviewId'), nullable=False)
    rating = db.Column (db.Integer)

    def __init__(self,voteId,voterId,rating):
        self.voteId = voteId
        self.voterId = voterId
        self.rating = rating

    def __repr__(self):
        return f'<Vote {self.voteId} {self.voterId} {self.year}{self.rating}>'

    def toJSON(self):
            return{
                'voteId': self.voteId,
                'voterId': self.voterId,
                'rating': self.rating
            }
    