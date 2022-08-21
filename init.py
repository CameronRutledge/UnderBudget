import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#Application Initialization
login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supahsecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app,db)

#Configure flask_login
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'You Must Sign In To Access This Page'
login_manager.login_message_category = 'danger'
