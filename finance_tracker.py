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

def get_user(user):
    id = User.query.filter_by(username=user).first()
    return id.user_id

def get_user_group(user):
    group = User.query.filter_by(username=user).first()
    return group

# functions
@app.route("/", methods=['GET', 'POST'])
def hello():
    return render_template("hello.html")


@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if "username" in session:
        group = User.query.filter_by(username=session['username']).first()
        return redirect(url_for("home", group=group.group, username=session["username"]))

    # log in
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("pass")
        password2 = request.form.get("pass2")
        
        if username == None or password == None or password2 == None:
            flash("please fill out all boxes before continuing")
            return render_template('signup.html')
        
        if password != password2:
            flash("passwords do not match")
            return render_template('signup.html')
        
        # check for duplicate username
        user = User.query.filter_by(username=username).first()
        if user is None: 
            group = 'user'
            db.session.add(User(username=username, password=password, group=group))
            db.session.commit()
            flash("registration complete. you may now log in.")
            return redirect('/signin')

        else:
            flash("we already have a user with that username. try something else!")
            return render_template('signup.html') 
    return render_template('signup.html')


@app.route("/signin", methods=['GET', 'POST'])
def signin():
    #check if already logged in, if so, go to home
    if "username" in session:
        group = User.query.filter_by(username=session['username']).first()
        return redirect(url_for("home", group=group.group, username=session["username"]))

    # log in 
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("pass")

        user = User.query.filter_by(username=username, password=password).first()
        if user is None:
            flash("incorrect username or password")
            return render_template('signin.html')
        else:
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['group'] = user.group
            return redirect(url_for("home", group=user.group, username=username))

    return render_template('signin.html')


# @app.route("/home", methods=['GET', 'POST'])
# @app.route("/home/<group>/", methods=['GET', 'POST'])
# @app.route("/home/<group>/<username>/", methods=['GET', 'POST'])
@app.route("/signout")
def signout():
    session.clear()
    return redirect('/')

app.secret_key = "AERTEYHO"
