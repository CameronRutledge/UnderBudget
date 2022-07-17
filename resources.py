from init import app, db
from models import User, Month, Expense
from flask_restful import Api,Resource
from flask_jwt import JWT ,jwt_required

jwt = JWT(app, authenticate, identity)
api = Api(app)
