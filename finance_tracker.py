# required imports
import os
import unittest
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
    client = db.Column(db.String(), default=0) # same as users username
    name = db.Column(db.String(), default = "") # name of expense
    date = db.Column(db.String(), unique=True)
    amount = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "<{}>".format(self.name)
    
class Income(db.Model):
    income_id = db.Column(db.Integer, primary_key=True)
    client = db.Column(db.String(), default=0) # same as users user_id
    name = db.Column(db.String(), default = "") # name of income
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
    # Admin 
    db.session.add(User(username='admin', password='password', group='admin')) # create default admin user
    db.session.commit() # commits database

def get_user(user):
    id = User.query.filter_by(username=user).first()
    return id.user_id

def get_user_group(user):
    group = User.query.filter_by(username=user).first()
    return group.group

def get_expenses(user):
    group = get_user_group(user)
    # personal user sees all of their own expenses
    if group == 'user':
        expenses = Expense.query.filter(Expense.client == user).order_by(Expense.date).all()
    # admin can see all expenses of users (????)**************
    else:  # group = "client"
        expenses = Expense.query.order_by(Expense.date).all()
    return expenses

def get_totalexpenses(user):
    totalexpense = db.session.query(db.func.sum(Expense.amount).filter(Expense.client == user)).scalar();
    return totalexpense;   

def get_totalincome(user):
    totalincome = db.session.query(db.func.sum(Income.amount)).filter(Income.client == user).scalar();
    return totalincome;  

def get_income(user):
    group = get_user_group(user)
    # personal user sees all of their own incomes
    if group == 'user':
        incomes = Income.query.filter(Income.client == user).order_by(Income.date).all()
    # admin can see all income of users (????)**************
    else:  # group = "admin"
        incomes = Income.query.order_by(Income.date).all()
    return incomes

# functions
@app.route("/", methods=['GET', 'POST'])
def hello():
    session.clear()
    return render_template("hello.html")
  

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if "username" in session:
        group = User.query.filter_by(username=session['username']).first()
        return redirect(url_for("home", group=group.group, username=session["username"]))

    # log in
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("password")
        password2 = request.form.get("password2")
        
        if not username or not password or not password2:
            flash("Please fill out all boxes before continuing!")
            return render_template('signup.html')
        
        if password != password2:
            flash("Passwords do not match!")
            return render_template('signup.html')
        
        # check for duplicate username
        user = User.query.filter_by(username=username).first()
        if user is None: 
            group = 'user'
            db.session.add(User(username=username, password=password, group=group))
            db.session.commit()
            flash("Registration complete. You may now log in.")
            return redirect('/signin')

        else:
            flash("A user exists with that username. Try something else.")
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
        password = request.form.get("password")

        user = User.query.filter_by(username=username, password=password).first()
        if user is None:
            flash("Incorrect username or password!")
            return render_template('signin.html')
        else:
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['group'] = user.group
            return redirect(url_for("home", group=user.group, username=username))

    return render_template('signin.html')


@app.route("/home", methods=['GET', 'POST'])
@app.route("/home/<group>/", methods=['GET', 'POST'])
@app.route("/home/<group>/<username>/", methods=['GET', 'POST'])
def home(group, username):
    expenses = get_expenses(username)
    income = get_income(username)
    return render_template('home.html', group = group, username = username, expenses = expenses, income = income)
  

@app.route("/enterexpense", methods=['GET', 'POST'])
def enterexpense():
    if request.method == "POST":
        username = request.form.get("user")
        date = request.form.get("date")
        name = request.form.get("name")
        amount = request.form.get("amount")

        if not date or not name or not amount:
            flash("Please make sure all fields are filled!")
            return redirect(url_for('record'))

                
        db.session.add(Expense(client=username, name=name, date=date, amount=amount))
        db.session.commit()
        # return redirect(url_for("home", group='user', username=username))
        return redirect(url_for('record'))

    # return redirect(url_for('home', group = 'user', username = username))
    return redirect(url_for('record'))

@app.route("/enterincome", methods=['GET', 'POST'])
def enterincome():
    if request.method == "POST":
        username = request.form.get("user")
        date = request.form.get("date")
        name = request.form.get("name")
        amount = request.form.get("amount")

        if not date or not name or not amount:
            flash("Please make sure all fields are filled!")
            return redirect(url_for('record'))
                
        db.session.add(Income(client=username, name=name, date=date, amount=amount))
        db.session.commit()
        # return redirect(url_for("home", group='user', username=username))
        return redirect(url_for('record'))

    # return redirect(url_for('home', group = 'user', username = username))
    return redirect(url_for('record'))


@app.route("/removeexpense", methods=['GET', 'POST'])
def removeexpense():
    username = request.form.get("user")
    e = Expense.query.filter(Expense.expense_id == request.form.get("expense_id")).first()
    db.session.delete(e)
    db.session.commit()
    # return redirect(url_for('home', group='user', username = username))
    return redirect(url_for('record'))

@app.route("/removeincome", methods=['GET', 'POST'])
def removeincome():
    username = request.form.get("user")
    i = Income.query.filter(Income.income_id == request.form.get("income_id")).first()
    db.session.delete(i)
    db.session.commit()
    # return redirect(url_for('home', group='user', username = username))
    return redirect(url_for('record'))


@app.route("/signout")
def signout():
    session.clear()
    return redirect('/')

@app.route("/record", methods=['GET', 'POST'])
@app.route("/record/<group>", methods=["GET", 'POST'])
@app.route("/record/<group>/<username>", methods=["GET", 'POST'])
def record():
    username = session['username']
    expenses = get_expenses(username)
    income = get_income(username)
    return render_template("record.html", group = 'user', username = username, expenses=expenses, income=income)
        
@app.route("/track", methods=['GET', 'POST'])
@app.route("/track/<group>", methods=["GET", 'POST'])
@app.route("/track/<group>/<username>", methods=["GET", 'POST'])
def track():
    username = session['username']
    totale = get_totalexpenses(username)
    totali = get_totalincome(username)
    expenses = get_expenses(username)
    income = get_income(username)
    return render_template("track.html", group = 'user', username = username, expenses=expenses, income=income, totale=totale, totali=totali)

app.secret_key = "AERTEYHO"
