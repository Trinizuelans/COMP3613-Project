from App.database import db
from flask import json

class Review (db.Model):
    reviewId = db.Column(db.Integer, primary_key=True)
    creatorId = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=False)
    studentId = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    votes = db.relationship('Vote',backref = db.backref('review',lazy = 'joined'))
    semesterId = db.Column(db.Integer, db.ForeignKey('semester.semesterId'), nullable=False)
    comment = db.Column(db.String(120), nullable = False) # staff must enter a message for review
    score = db.Column(db.Numeric(precision=10, scale=2), default = 0)
    upvote = db.Column(db.Integer)
    downvote = db.Column(db.Integer)
    votebalance = db.Column(db.Integer)

    # creator = db.relationship('Staff',backref = db.backref('review',lazy = 'joined'))
    # student = db.relationship('Student',backref = db.backref('review',lazy = 'joined'))

    def __init__(self,creatorId,studentId,comment,semesterId,score):
            self.creatorId = creatorId
            self.studentId = studentId
            self.votes = []
            self.semesterId = semesterId 
            self.comment = comment
            self.score = score
            self.upvote = 0
            self.downvote = 0
            self.votebalance = 0

    def __repr__(self):
        return f'<Review {self.reviewId} {self.creatorId} {self.studentId} {self.votes} {self.semesterId} {self.comment}{self.score}{self.upvote}{self.downvote}{self.votebalance}>'

    def toJSON(self):
            from App.controllers.vote import (getVotesByReviewId_JSON)
            return{
                'reviewId': self.reviewId,
                'creatorId': self.creatorId,
                'studentId': self.studentId,
                'votes': getVotesByReviewId_JSON(self.reviewId),
                'semester': self.semesterId,
                'comment': self.comment,
                'score' : self.score,
                'upvote': self.upvote,
                'downvote': self.downvote,
                'votebalance': self.votebalance
            }
    