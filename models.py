from Budget_Keeper import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
