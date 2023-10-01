import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users )
from App.controllers import(update_student_year, update_student_programme,calcAvgReviewScore,getRatedReviews)
from App.controllers import(addStudent,addStaff,addSemester,addReview,addVote,addReviewVotes,getAllReviews_JSON)
from datetime import date

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    staff = addStaff(735,"John","Doe","john.doe@sta.uwi.edu","johnpass")
    staff = addStaff(738,"Bob","Doe","bob.doe@sta.uwi.edu","bobpass")
    student = addStudent(816,"Sally","Shell","sally.shell@my.uwi.edu",2,"BSc Computer Science (Special)")
    newSemester = addSemester("SEM1",2023,date(2023,8,25),date(2023,12,25))

    newReview = addReview(735,816,1,"Sally sleeps in every class of mine!",-1)
    newVote = addVote(738,1,2)
    addvote = addReviewVotes(1)
    newReview.score = calcAvgReviewScore(newReview.reviewId)
    

    newReview1 = addReview(738,816,1,"Sally is a bad student!",-2)
    newVote = addVote(735,2,3)
    addvote = addReviewVotes(2)
    newReview1.score = calcAvgReviewScore(newReview1.reviewId)
    print(newReview1.score)

    reviews = getAllReviews_JSON()
    print(reviews)
    print('database intialized')

'''
User Commands

'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a staff user")
@click.argument("id", default="1")
@click.argument("firstName", default="rob")
@click.argument("lastName", default="Me")
@click.argument("email", default="rob.me@sta.uwi.edu")
@click.argument("password", default="robpass")
def create_user_command(id,firstName,lastName,email, password):
    # create_user(username, password)
    staff = addStaff(id,firstName,lastName,email, password)
    print(f'{staff.firstName} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

@user_cli.command("UpdateYear", help="Updates Student year")
@click.argument("id", default="1")
@click.argument("year", default="1")
def update_year_command(id,year):
     update_student_year(id, year)

@user_cli.command("UpdateProgramme", help="Updates Student programme")
@click.argument("id", default="1")
@click.argument("prog", default="Computer Science General")
def update_prog_command(id,prog):
     update_student_programme(id, prog)

@user_cli.command("getStudRevs", help="gets student reviews")
@click.argument("id", default="1")
def get_rev_command(id):
     revs = getRatedReviews(id)
    

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)