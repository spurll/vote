from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[DataRequired()])
    remember = BooleanField("Remember Me", default=True)

class VoteForm(FlaskForm):
    ballot = HiddenField(validators=[DataRequired()])
