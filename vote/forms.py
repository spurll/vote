from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, HiddenField
from wtforms.validators import Required


class LoginForm(Form):
    username = TextField("Username", validators=[Required()])
    password = PasswordField("Password", validators=[Required()])
    remember = BooleanField("Remember Me", default=False)

class VoteForm(Form):
    ballot = HiddenField()
