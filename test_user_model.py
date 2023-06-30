"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows
from sqlalchemy.exc import IntegrityError
# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1",
                         "test1@gmail.com",
                         "HASHED_PASSWORD",
                         None)
        uid1 = 11111
        u1.id = uid1
        u2 = User.signup("test2",
                         "test2@gmail.com",
                         "HASHED_PASSWORD",
                         None)
        uid2 = 22222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res     

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
    
    def test_repr(self):
       
        u = User(id=124213,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        expected_repr = "<User #124213: testuser, test@test.com>"
        self.assertEqual(repr(u), expected_repr)

# Follow Tests
    def test_is_following(self):
        self.u1.following.append(self.u2)
        db.session.commit()


        # is_following detect when u1 is following u2
        self.assertIn(self.u2, self.u1.following)

        # is_following detect when u1 is not following u2
        self.u1.following.remove(self.u2)
        self.assertNotIn(self.u2, self.u1.following)

    def test_is_followed_by(self):

        # is_followed_by detect when u1 is followed by u2
        self.u1.followers.append(self.u2)
        self.assertIn(self.u2, self.u1.followers)

        # is_followed_by detect when u1 is not followed by u2
        self.u1.followers.remove(self.u2)
        self.assertNotIn(self.u2, self.u1.followers)

# Sign Up Tests
    def test_user_sign_up_success(self):
        valid = User.signup(
            'testtest',
            'testest@test.com',
            'HASHED_PASSWORD',
            None
        )
        uid_test = 33333
        valid.id = uid_test
        # To see if it works.
        db.session.commit()
    
    def test_user_sign_up_username_fail(self):
        invalid_test = User.signup(
            None,
            "Test@test.com",
            "HASHED_PASSWORD",
            None)
        uid_test = 12341234
        invalid_test.id = uid_test    
        # Username is already taken. Ensure that the IntegrityError is raised
        with self.assertRaises(IntegrityError):
            db.session.commit()
    
    def test_user_sign_up_password_fail(self):
        # Password Fail: Ensure that the ValueError is raised
        
        # To see if password is empty
        with self.assertRaises(ValueError):
            User.signup(
                'testtest',
                'test@testtest.com',
                "",
                None
            )
        
        with self.assertRaises(ValueError):
            User.signup(
                'testtest',
                'test@testtest.com',
                None,
                None
            )      
# Authenticate Tests
#         
    def test_user_authenticate(self):
        # To see if username and password are correct
        self.assertTrue(User.authenticate(self.u1.username, "HASHED_PASSWORD"))
    
    def test_user_authenticate_fail_username(self):
        # To see if username is incorrect
        self.assertFalse(User.authenticate("Fake", "HASHED_PASSWORD"))
        
    def test_user_authenticate_fail_password(self):
        # To see if password is incorrect
        self.assertFalse(User.authenticate(self.u1.username, "HASHED"))

