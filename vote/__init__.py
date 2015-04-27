from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"


from vote.controller import VoteController
api = VoteController(
    selection=app.config['SELECTION'],
    winners=app.config['WINNERS'],
    premium_limit=app.config['PREMIUM_LIMIT']
)


#from vote import views, models
