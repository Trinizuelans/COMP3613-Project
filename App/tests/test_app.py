import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    get_student,
    addStudent,
    update_student,
    addStaff,
    get_staff,
    addReview,
    addVote,
    getReview,
    updateVote
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"


class StudentIntegrationTests(unittest.TestCase):

    def test_add_student(self):
        New_student = addStudent (817,"Ally","Sam","ally@mail.con",3,"Computer Science (Special)")
        Search_student = get_student(817)
        assert Search_student.firstName == "Ally"

    def test_search_student(self):
        student =  get_student(817)
        assert student.firstName == "Ally"

    def test_update_student(self):
        Search_student = get_student(817)
        Update_student = update_student(Search_student.id, "Hally", "Ham", "hally@mail.com", 3, "Computer Science (General)")
        assert Update_student.firstName == "Hally"
        
class ReviewIntegrationTests(unittest.TestCase): 

    def testA_add_staff(self):
        New_staff = addStaff (739, "Phaedra", "Mohammed", "phae@mail.com", "phaepass")
        assert New_staff.firstName == "Phaedra"

    def testB_log_review(self):
        Creator = get_staff(739)
        New_review = addReview(Creator.id,817,1,"Ally is a good mango",3)
        assert New_review.creatorId == 739 and New_review.studentId == 817 

    def testC_upvote_review(self):
        New_staff = addStaff (740, "Perm", "Mohan", "perm@mail.com", "permpass")
        New_vote = addVote(740,3,3,upvote = True)
        assert New_vote.voterId == 740 and New_vote.rating == 3 and New_vote.upvote == True

    def testD_downvote_review(self):
        New_staff = addStaff (741, "Nick", "Mendez", "nick@mail.com", "nickpass")
        New_vote = addVote(741,3,2,upvote = False)
        assert New_vote.voterId == 741 and New_vote.rating == 2 and New_vote.upvote == False

    def testE_updatevote_review(self):
        Updated_vote = updateVote(3,3,True)
        assert Updated_vote.voterId == 741 and Updated_vote.rating == 3 and Updated_vote.upvote == True and Updated_vote.voteId == 3
        

    

    



     