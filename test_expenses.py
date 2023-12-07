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

    # test for the tracking page
    def test_income(self):
        # sign up
        self.app.post('/signup', data=dict(
            user='testuser',
            password='testpassword',
            password2='testpassword'
        ), follow_redirects=True)

        # log in
        self.app.post('/signin', data=dict(
            user='testuser',
            password='testpassword'
        ), follow_redirects=True)

        # enter income
        response = self.app.post('/enterincome', data=dict(
            user='testuser',
            name='Salary',
            amount='5000',
            date='2023-12-06'
        ), follow_redirects=True)

        # income is displayed on the page
        self.assertIn(b'Salary', response.data)
        self.assertIn(b'$5000', response.data)
        self.assertIn(b'2023-12-06', response.data)

        # sign out
        response = self.app.get('/signout', follow_redirects=True)
        self.assertNotIn(b'Logged in as', response.data)
        self.assertIn(b'Sign In Here!', response.data)

    # test for recording page
    def test_view_record_expenses(self):
        # sign up
        self.app.post('/signup', data=dict(
            user='testuser',
            password='testpassword',
            password2='testpassword'
        ), follow_redirects=True)

        # log in
        self.app.post('/signin', data=dict(
            user='testuser',
            password='testpassword'
        ), follow_redirects=True)

        # expense
        self.app.post('/enterexpense', data=dict(
            user='testuser',
            name='Christmas',
            amount='100',
            date='2023-12-06'
        ), follow_redirects=True)

        # record 
        response = self.app.get('/record', follow_redirects=True)

        # entered expense is on page
        self.assertIn(b'Christmas', response.data)
        self.assertIn(b'$100', response.data)
        self.assertIn(b'2023-12-06', response.data)

        # sign out
        response = self.app.get('/signout', follow_redirects=True)
        self.assertNotIn(b'Logged in as', response.data)
        self.assertIn(b'Sign In Here!', response.data)


if __name__ == '__main__':
    unittest.main()
