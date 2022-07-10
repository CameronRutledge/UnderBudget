from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from models import User

#Create User Form
class RegistrationForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(),Email()])
    password = PasswordField('Password:', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm Password:', validators=[DataRequired()])
    submit = SubmitField('Register!')

    #Email Registration Check
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Your email has been registered already!')

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Log In')
