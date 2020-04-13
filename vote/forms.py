from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, BooleanField, HiddenField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    username = TextField("Username:", validators=[Required()])
    password = PasswordField("Password:", validators=[Required()])
    remember = BooleanField("Remember Me", default=True)

class VoteForm(FlaskForm):
    ballot = HiddenField(validators=[Required()])
