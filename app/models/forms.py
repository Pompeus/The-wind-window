from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length,Regexp

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators= [DataRequired()])
    remember_me = BooleanField('remeber_me')

class Register(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(),Length(min=8, message= 'Password must be at least 8 chearcters long'),Regexp(r'.*[0-9].*', message='Password must contain last one number'), Regexp(r'.*[^a-zA-Z0-9\s].*', message= 'Password must at one special chearcter')])
    confirm_pass = PasswordField('confirm_pass', validators=[DataRequired()])
