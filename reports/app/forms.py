from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired
from app.src import *

class PBBForm(FlaskForm):
    proj = SelectField('project', validators=[DataRequired()])
    branch = SelectField('branch', validators=[DataRequired()])
    build = SelectField('build', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(PBBForm, self).__init__(*args, **kwargs)
        self.proj.choices = state.dd.proj.choices
        self.branch.choices = state.dd.branch.choices
        self.build.choices = state.dd.build.choices

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class EmailForm(FlaskForm):
    recipient = StringField("to", validators=[DataRequired()])
    subject = StringField("subject", validators=[DataRequired()])
    message = TextAreaField("message", validators=[DataRequired()])
    submit = SubmitField("Submit")