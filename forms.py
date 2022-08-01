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
    pass_confirm = PasswordField(validators=[DataRequired('Please Re-Enter Your Password')])
    create_account = SubmitField('Create Account')

    #Email Registration Check
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('This Email Is Already Associated With An Account')

class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired('Please Enter An Email Address'), Email('Please Enter A Valid Email Address')])
    password = PasswordField(validators=[DataRequired('Please Enter A Password')])
    login = SubmitField('Sign In')


class SavingsForm(FlaskForm):
    salary = IntegerField(validators=[DataRequired('Please Enter Your Salary')])
    savings_goal = IntegerField(validators=[DataRequired('Please Enter Your Savings Goal')])
    savings_date = DateField(format='%Y-%m', validators=[DataRequired('Please Enter Your Savings Deadline')])
    savings_submit = SubmitField('Save Goal')

class ExpenseForm(FlaskForm):
    expense_type = SelectField('Expense Type', choices=[('Housing','Housing'), ('Transportation', 'Transportation'), ('Food', 'Food'), ('Entertainment', 'Entertainment'), ('Misc.', 'Misc.')])
    cost = IntegerField('Expense Cost', validators=[DataRequired('Please Enter The Cost of Your Expense')])
    expense_submit = SubmitField('Add Expense')

class EditForm(FlaskForm):
    expense_type = SelectField('Expense Type', choices=[('Housing','Housing'), ('Transportation', 'Transportation'), ('Food', 'Food'), ('Entertainment', 'Entertainment'), ('Misc.', 'Misc.')])
    cost = IntegerField('Expense Cost', validators=[DataRequired('You Cannot Remove The Cost')])
    expense_id = StringField()
    update_expense = SubmitField('Update')
    remove_expense = SubmitField('Delete')
