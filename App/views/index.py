from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.models import db, SemNum,Faculty
from App.controllers import *
from datetime import date

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.route('/init', methods=['GET'])
def init():
    db.drop_all()
    db.create_all()

    #sample data
    addStaff(101,'bob',"Frank","bobfrank@sta.uwi.edu", 'bobpass')
    staff = addStaff(735,"John","Doe","john.doe@sta.uwi.edu","johnpass")
    staff = addStaff(738,"Bob","Doe","bob.doe@sta.uwi.edu","bobpass")
    student = addStudent(816,"Sally","Shell","sally.shell@my.uwi.edu",2,"BSc Computer Science (Special)","FST")
    newSemester = addSemester(SemNum.SEM1,2023,date(2023,8,25),date(2023,12,25))
    newSemester2 = addSemester(SemNum.SEM2,2024,date(2024,1,21),date(2024,5,10))
    summer  = addSemester(SemNum.SEM3,2024,date(2024,5,19),date(2024,7,26))

    newReview = addReview(735,816,"Sally sleeps in every class of mine!",-1)
    newVote = addVote(738,1,2,False)
    addvote = addReviewVotes(1)
    newReview.score = calcAvgReviewScore(newReview.reviewId)
    

    newReview1 = addReview(738,816,"Sally is a bad student!",-2)
    newVote = addVote(735,2,3, False)
    addvote = addReviewVotes(2)
    newReview1.score = calcAvgReviewScore(newReview1.reviewId)
    return jsonify(message='db initialized!')

@index_views.route('/reset', methods=['GET'])
def delete():
    db.drop_all()
    return jsonify(message='db reset!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})