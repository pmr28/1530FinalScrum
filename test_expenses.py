import os
import unittest
from flask import Flask, session
from finance_tracker import app, db, User

class FinanceTrackerTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_registration(self):
        response = self.app.post('/signup', data=dict(
            user='testuser',
            password='testpassword',
            password2='testpassword'
        ), follow_redirects=True)
        self.assertIn(b'Registration complete. You may now log in.', response.data)

    # test for usernames that already exist when signing up
    def test_duplicate_user(self):
        response = self.app.post('/signup', data=dict(
            user='testuser',
            password='testpassword',
            password2='testpassword'
        ), follow_redirects=True)

        response = self.app.post('/signup', data=dict(
            user='testuser',
            password='testpassword',
            password2='testpassword'
        ), follow_redirects=True)
        self.assertIn(b'A user exists with that username. Try something else.', response.data)

    def test_login(self):
        # sign up
        self.app.post('/signup', data=dict(
            user='testuser',
            password='testpassword',
            password2='testpassword'
        ), follow_redirects=True)

        # log in
        response = self.app.post('/signin', data=dict(
            user='testuser',
            password='testpassword'
        ), follow_redirects=True)
        self.assertIn(b'testuser', response.data)

        # sign out
        response = self.app.get('/signout', follow_redirects=True)
        self.assertNotIn(b'Logged in as', response.data)
        self.assertIn(b'Sign In Here!', response.data)

if __name__ == '__main__':
    unittest.main()
