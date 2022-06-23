

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField 
from wtforms.validators import InputRequired, Length, Email
from wtforms.widgets import TextArea


class UserForm(FlaskForm):
    """Form for creating new User"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)])
    email = EmailField("Email", validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    """Form for users to login"""
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)])

class FeedbackForm(FlaskForm):
    """Form for adding/editing a specified users feedback"""

    title = StringField('Title', validators=[InputRequired(), Length(max=100)])
    content = StringField('Content', widget=TextArea(), validators=[InputRequired()])      
   