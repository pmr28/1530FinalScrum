# required imports
import os
from flask import Flask, request, url_for, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import jinja2

db = SQLAlchemy()
app = Flask(__name__)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True) # number id given to user
    username = db.Column(db.String(20), unique=True) # username max length is 20
    password = db.Column(db.String(20)) # password max length is 20
    group = db.Column(db.String(10)) # either admin or user

    def __repr__(self):
        return "<{}>".format(self.username)


class Expense(db.Model):
    expense_id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(20), default=0) # same as users username
    name = db.Column(db.String(30), default = "") # name of expense
    date = db.Column(db.String(), unique=True)
    amount = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "<{}>".format(self.name)
    
class Income(db.Model):
    income_id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.Integer, default=0) # same as users user_id
    name = db.Column(db.String(30), default = "") # name of income
    date = db.Column(db.String(), unique=True)
    amount = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "<{}>".format(self.name)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance_tracker.db"
db.init_app(app)


# create database within initdb

@app.cli.command('initdb')
def initdb():
    db.drop_all() # remove all previous data (therefore does not currently last over nultiple sessions)
    db.create_all() # create our models
    db.session.add(User(username='admin', password='password', group='admin')) # create default admin user
    db.session.commit() # commits database


# functions
@app.route("/", methods=['GET', 'POST'])
def hello():
    return render_template("hello.html")

app.secret_key = "AERTEYHO"