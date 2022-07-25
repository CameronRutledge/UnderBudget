from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from models import User

#Create User Form
class RegistrationForm(FlaskForm):
    name = StringField(validators=[DataRequired('Please Enter Your Name')])
    email = StringField(validators=[DataRequired('Please Enter A Valid Email Address'),Email('Please Enter A Valid Email Address')])
    password = PasswordField(validators=[DataRequired('Please Enter A Password'), EqualTo('pass_confirm', message='Passwords Do Not Match. Please Re-Enter Your Password')])
    pass_confirm = PasswordField(validators=[DataRequired('Please Confirm Your Password')])

    #Email Registration Check
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('This Email Is Already Associated With An Account')

class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired('Please Enter An Email Address'), Email('Please Enter A Valid Email Address')])
    password = PasswordField(validators=[DataRequired('Please Enter A Password')])


class SavingsForm(FlaskForm):
    salary = IntegerField(validators=[DataRequired('Please Enter Your Salary')])
    savings_goal = IntegerField(validators=[DataRequired('Please Enter Your Savings Goal')])
    savings_date = DateField(format='%Y-%m', validators=[DataRequired('Please Enter Your Savings Deadline')])

class ExpenseForm(FlaskForm):
    expense_type = SelectField('Expense Type', choices=[(1,'Housing'), (2, 'Transportation'), (3, 'Food'), (4, 'Entertainment'), (5, 'Misc.')], validators=[DataRequired('Please Enter The Cost of Your Expense')])
    cost = IntegerField('Expense Cost', validators=[DataRequired('Please Enter The Cost of Your Expense')])
