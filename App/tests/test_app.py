import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User,Faculty
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
    get_staff_JSON,
    getReview,
    updateVote,
    addDownVote,
    addUpvote,
    format_faculty
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''


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
    user = addStaff(2,"Rob","Ben","robben@mail.com","robpass")
    assert login(2, "robpass") != None

# class UsersIntegrationTests(unittest.TestCase):

#     def test_create_user(self):
#         user = create_user("rick", "bobpass")
#         assert user.username == "rick"

#     def test_get_all_users_json(self):
#         users_json = get_all_users_json()
#         self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

#     # Tests data changes in the database
#     def test_update_user(self):
#         update_user(1, "ronnie")
#         user = get_user(1)
#         assert user.username == "ronnie"

class StaffIntegrationTests(unittest.TestCase):

    def testA_new_user(self):
        creatorId = 1
        firstName = "Bob"
        lastName = "Test"
        email = "bob@mail.com"
        password = "bobpass"
        
        new_staff = addStaff (creatorId, firstName, lastName, email, password)
        
        assert new_staff.id == 1

    # pure function no side effects or integrations called
    def testB_get_json(self):
        staff = get_staff_JSON(1)
        self.assertDictEqual(staff, 
            {'staffid': 1,'firstName': "Bob",
            'lastName': "Test",
            'email': "bob@mail.com",
            'reviews': []})
    
    def testC_hashed_password(self):
        password = "bobpass"
        hashed = generate_password_hash(password, method='sha256')
        staff = get_staff(1)
        assert staff.password != password

    def testD_check_password(self):
        password = "bobpass"
        staff = get_staff(1)
        assert staff.check_password(password)


class StudentIntegrationTests(unittest.TestCase):

    def testA_add_student(self):
        studentId = 817
        firstName = "Ally"
        lastName = "Sam"
        email = "ally@mail.com"
        year = 3
        programme = "Computer Science (General)"
        faculty = "FST"
        f = format_faculty(faculty)

        new_student = addStudent (studentId,firstName,lastName,email,year,programme,"FST")

        assert new_student is not None, "Student creation failed."
        assert new_student.firstName == firstName, f"Expected firstName: {firstName}, Actual: {new_student.firstName}"
        assert new_student.lastName == lastName, f"Expected lastName: {lastName}, Actual: {new_student.lastName}"
        assert new_student.email == email, f"Expected email: {email}, Actual: {new_student.email}"
        assert new_student.year == year, f"Expected year: {year}, Actual: {new_student.year}"
        assert new_student.programme == programme, f"Expected email: {programme}, Actual: {new_student.programme}"
        assert new_student.faculty == f, f"Expected faculty: {f}, Actual: {new_student.faculty}"

    def testB_search_student(self):
        studentId = 817

        student =  get_student(817)

        assert student is not None, "Student search failed."
        assert student.id == studentId, f"Expected creatorId: {studentId}, Actual: {student.id}"


    def testC_update_student(self):
        studentId = 817
        firstName = "Hally"
        lastName = "Ham"
        email = "hally@mail.com"
        year = 3
        programme = "Computer Science (General)"

        updated_student = update_student(studentId,firstName,lastName,email,year,programme)

        assert updated_student is not None, "Student update failed."
        assert updated_student.firstName == firstName, f"Expected firstName: {firstName}, Actual: {updated_student.firstName}"
        assert updated_student.lastName == lastName, f"Expected lastName: {lastName}, Actual: {updated_student.lastName}"
        assert updated_student.email == email, f"Expected email: {email}, Actual: {updated_student.email}"
        
class ReviewIntegrationTests(unittest.TestCase): 

    def testA_add_staff(self):
        creatorId = 739
        firstName = "Phae"
        lastName = "Mohammed"
        email = "phae@mail.com"
        password = "phaepass"
        
        new_staff = addStaff (creatorId, firstName, lastName, email, password)
        
        assert new_staff is not None, "Staff creation failed."
        assert new_staff.id == creatorId, f"Expected creatorId: {creatorId}, Actual: {new_staff.id}"
        assert new_staff.firstName == firstName, f"Expected firstName: {firstName}, Actual: {new_staff.firstName}"
        assert new_staff.lastName == lastName, f"Expected lastName: {lastName}, Actual: {new_staff.lastName}"
        assert new_staff.email == email, f"Expected email: {email}, Actual: {new_staff.email}"
        

    def testB_log_review(self):
        creatorId = 739
        studentId = 817
        semesterId = 1
        comment = "Great student"
        rating = 3

        creator = get_staff(creatorId)
        new_review = addReview(creator.id, studentId, comment, rating,semesterId)

        assert creator is not None, "Creator retrieval failed."
        assert new_review is not None, "Review creation failed."
        assert new_review.creatorId == creatorId, f"Expected creatorId: {creatorId}, Actual: {new_review.creatorId}"
        assert new_review.studentId == studentId, f"Expected studentId: {studentId}, Actual: {new_review.studentId}"
        assert new_review.comment == comment, f"Expected Rating: {comment}, Actual: {new_review.comment}"
        assert new_review.score== rating, f"Expected Score: {rating}, Actual: {new_review.score}"
        assert new_review.semesterId== semesterId, f"Expected semesterId: {semesterId}, Actual: {new_review.semesterId}"
     

    def testC_upvote_review(self):
        voterId = 740
        reviewId = 1

        new_staff = addStaff(voterId, "Perm", "Mohan", "perm@mail.com", "permpass")
        review = getReview(reviewId)
        new_vote = addUpvote(voterId,  reviewId)

        assert new_staff is not None, "Staff creation failed."
        assert review is not None, "Review retrieval failed."
        assert new_vote is not None, "Upvote creation failed."
        assert new_vote.voterId == voterId, f"Expected voterId: {voterId}, Actual: {new_vote.voterId}"
        assert new_vote.rating == review.votes[0].rating, f"Expected rating: {review.votes[0].rating}, Actual: {new_vote.rating}"
        assert new_vote.upvote, "Expected upvote: True, Actual: False"


    def testD_downvote_review(self):
        voter_id = 741
        review_id = 1
        rating = 2

        new_staff = addStaff(voter_id, "Nick", "Mendez", "nick@mail.com", "nickpass")
        new_vote = addDownVote(voter_id, review_id, rating)

        assert new_staff is not None, "Staff creation failed."
        assert new_vote is not None, "Downvote creation failed."
        assert new_vote is not "Duplicate", "Multiple votes attempted by Staff for a review!"
        assert new_vote is not "Invalid", "Invalid Rating entered."
        assert new_vote.voterId == voter_id, f"Expected voterId: {voter_id}, Actual: {new_vote.voterId}"
        assert new_vote.rating == rating, f"Expected rating: {rating}, Actual: {new_vote.rating}"
        assert not new_vote.upvote, "Expected upvote: False, Actual: True"

    def testE_updatevote_review(self):
        voter_id = 741
        vote_id = 3
        new_rating = 3
        new_upvote = True

        updated_vote = updateVote(vote_id,new_rating, new_upvote)

        assert updated_vote.voterId == voter_id, f"Expected voterId to be {voter_id}, but got {updated_vote.voterId}"
        assert updated_vote.rating == new_rating, f"Expected rating to be {new_rating}, but got {updated_vote.rating}"
        assert updated_vote.upvote == new_upvote, f"Expected upvote to be {new_upvote}, but got {updated_vote.upvote}"
        assert updated_vote.voteId == vote_id, f"Expected voteId to be {vote_id}, but got {updated_vote.voteId}"


    

    



     