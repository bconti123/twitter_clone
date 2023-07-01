"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python3 -m unittest -v test_user_views.py

import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        db.session.commit()
        
    # Follower Page Tests
    def test_follower_page_login(self):
        """Logged in, can see follower page? """

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.get(f'/users/{self.testuser_id}/followers')
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Access unauthorized.", str(resp.data))
    
    def test_follower_page_logged_out(self):
        """Logged out, disallowed from follower page? """

        with self.client as c:
            resp = c.get(f'/users/{self.testuser_id}/followers', follow_redirects=True)

            self.assertIn("Access unauthorized.", str(resp.data))
    
    # Following Page Tests
    def test_following_page_login(self):
        """Logged in, can see following page? """
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.get(f'/users/{self.testuser_id}/following')
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Access unauthorized.", str(resp.data))
    
    def test_following_page_logged_out(self):
        """Logged out, disallowed from following page? """

        with self.client as c:
            resp = c.get(f'/users/{self.testuser_id}/following', follow_redirects=True)

            self.assertIn("Access unauthorized.", str(resp.data))
    
    ## Homepage Tests
    def test_homepage_logged_in(self):
        """ Logged in, you can see the message list in homepage? """
        
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.get('/')
            # Ensure the message list is appeared
            self.assertIn('list-group', str(resp.data))
            self.assertIn('messages', str(resp.data))
    
    def test_homepage_logged_in(self):
        """ Logged out, disallowed from the message list in homepage? """

        with self.client as c:
            resp = c.get('/')
            # Ensure the message list does not exist
            self.assertNotIn('list-group', str(resp.data))
            self.assertNotIn('messages', str(resp.data))
    
    def test_404_page(self):
        """ Can see 404 page? If any query is not existed """

        with self.client as c:
            resp = c.get(f'/users/9999999999')
            self.assertIn('Sorry', str(resp.data))
            self.assertEqual(resp.status_code, 404)

            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            
            resp = c.get(f'/users/999999999/following')
            self.assertIn('Sorry', str(resp.data))
            self.assertEqual(resp.status_code, 404)

            resp = c.get(f'/users/999999999/followers')
            self.assertIn('Sorry', str(resp.data))
            self.assertEqual(resp.status_code, 404)

            resp = c.post(f'/users/follow/9999999')
            self.assertIn('Sorry', str(resp.data))
            self.assertEqual(resp.status_code, 404)

            resp = c.post(f'/users/stop-following/9999999')
            self.assertIn('Sorry', str(resp.data))
            self.assertEqual(resp.status_code, 404)