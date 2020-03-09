from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, SelectField, TextAreaField, TextField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators = [Length(min=4, max=25)])
    email = StringField('Email Address', validators = [Length(min=6, max=35), Email()])
    password = PasswordField('New Password', validators = [DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Register')

class JourneyInfoForm(FlaskForm):
    username = StringField('Username', validators = [Length(min=4, max=25)]) 
    submit = SubmitField('Submit')