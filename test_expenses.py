import unittest
from flask import Flask
from flask_testing import TestCase
from finance_tracker import app, db, User, Expense, Income, initdb
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_


class expenseTest(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_signup(self):
        response = self.client.post('/signup', data=dict(user='new_user', password='password', password2='password'), follow_redirects=True)
        assert b'Registration complete' in response.data

    def test_signin(self):
        response = self.client.post('/signin', data=dict(user='admin',password='password'), follow_redirects=True)

        assert b'Welcome, admin' in response.data

    def test_enterexpense(self):
        self.client.post('/signin', data=dict(user='admin',password='password'), follow_redirects=True)

        response = self.client.post('/enterexpense', data=dict(user='admin',date='2023-01-01',name='Test Expense',amount=100), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Expense recorded successfully', response.data)
      
if __name__ == '__main__':
    unittest.main()