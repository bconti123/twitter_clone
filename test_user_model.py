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

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

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

    def test_is_following(self):

        u1 = User(id=12343,
                email="test1@test.com",
                username="test1user",
                password="HASHED_PASSWORD")
        
        u2 = User(id=12341,
                email="test2@test.com",
                username="test2user",
                password="HASHED_PASSWORD")
                
        db.session.add(u1, u2)
        db.session.commit()

        # is_following detect when u1 is following u2
        u1.following.append(u2)
        expected_following = '<User #12341: test2user, test2@test.com>'
        self.assertEqual(repr(u1.following[0]), expected_following)

        # is_following detect when u1 is not following u2
        u1.following.remove(u2)
        self.assertNotIn(u2, u1.following)

    def test_is_followed_by(self):

        u1 = User(id=12343,
                email="test1@test.com",
                username="test1user",
                password="HASHED_PASSWORD")
        
        u2 = User(id=12341,
                email="test2@test.com",
                username="test2user",
                password="HASHED_PASSWORD")
                
        db.session.add(u1, u2)
        db.session.commit()
        # is_followed_by detect when u1 is followed by u2
        u1.followers.append(u2)
        self.assertIn(u2, u1.followers)

        # is_followed_by detect when u1 is not followed by u2
        u1.followers.remove(u2)
        self.assertNotIn(u2, u1.followers)
    
    def test_user_sign_up_success_and_fail(self):

        User.signup(
            email="test1@test.com",
            username="test1user",
            password="HASHED_PASSWORD",
            image_url=User.image_url.default.arg)
            
        db.session.commit()

        # Username is already taken. Ensure that the IntegrityError is raised
        with self.assertRaises(IntegrityError):
            u1 = User.signup(
                email="test21@test.com",
                username="test1user",
                password="2132123124",
                image_url=User.image_url.default.arg)

            # Commit the changes to trigger the IntegrityError
            db.session.commit()
        
        # Password Fail: Ensure that the ValueError is raised
        with self.assertRaises(ValueError):
            User.signup(
                email="test21@test.com",
                username="test12user",
                password=None,
                image_url=User.image_url.default.arg)
            
            # Commit the changes to trigger the ValueError
            db.session.commit()
        
        
    def test_user_authenticate(self):
        
        User.signup(
            email="test1@test.com",
            username="test1user",
            password="HASHED_PASSWORD",
            image_url=User.image_url.default.arg)
            
        db.session.commit()

        valid = User.authenticate("test1user", "HASHED_PASSWORD")

        self.assertTrue(valid)
    
    def test_user_authenticate_fail_username(self):
        User.signup(
            email="test1@test.com",
            username="test1user",
            password="HASHED_PASSWORD",
            image_url=User.image_url.default.arg)
            
        db.session.commit()

        invalid = User.authenticate("test", "HASHED_PASSWORD")
        
        self.assertFalse(invalid)

    def test_user_authenticate_fail_password(self):

        User.signup(
            email="test1@test.com",
            username="test1user",
            password="HASHED_PASSWORD",
            image_url=User.image_url.default.arg)
            
        db.session.commit()

        invalid = User.authenticate("test1user", "HASHED")
        
        self.assertFalse(invalid)


