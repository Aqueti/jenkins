from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class PBBForm(FlaskForm):
    proj = SelectField('project', choices=[(0,'ACOS')])
    branch = SelectField('branch', choices=[(0,'master'), (1,'beta'), (2,'dev')])
    build = SelectField('build', choices=[(1,1), (2,2), (3,3)])
