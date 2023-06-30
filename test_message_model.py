"""User model tests."""

# run these tests like:
#
#    python3 -m unittest test_message_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

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


class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()
        u = User(
            id=12341234,
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )
        m = Message(
            text='Hello!'
        )
        u.messages.append(m)
        db.session.add(u)
        db.session.commit()

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):

        """Does basic model work?"""
        u = User.query.get(12341234)
        # Check if user added message
        self.assertEqual(len(u.messages), 1)
    
    def test_message_delete(self):

        u = User.query.get(12341234)

        # pop()/remove() delete message
        u.messages.pop()
        # Check if user deleted message works?
        self.assertEqual(len(u.messages), 0)
    

    
