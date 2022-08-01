from init import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import date

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique = True, index = True)
    password_hash = db.Column(db.String)
    salary = db.Column(db.Integer)
    savings_goal = db.Column(db.Integer)
    date_created = db.Column(db.Date)
    savings_date = db.Column(db.Date)

    #Relationships
    months = db.relationship('Month', backref='user', lazy='dynamic')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.date_created = date.today()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Month(db.Model):

    month_id = db.Column(db.Integer, primary_key = True)
    month = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #Relationships
    expenses = db.relationship('Expense', backref='month', lazy='dynamic')

    def __init__(self, month, user_id):
        self.month = month
        self.user_id = user_id

class Expense(db.Model):

    expense_id = db.Column(db.Integer, primary_key = True)
    expense_type = db.Column(db.Text)
    cost = db.Column(db.Integer)
    date = db.Column(db.Date)
    month_id = db.Column(db.Integer, db.ForeignKey('month.month_id'))

    def __init__(self, expense_type, cost, date, month_id):
        self.expense_type = expense_type
        self.cost = cost
        self.date = date
        self.month_id = month_id
