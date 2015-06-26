from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


# Ensure that tables are created. The order in which this occurs is important:
# 1. Initialize the SQLAlchemy object.
# 2. Import the models. (The schema will need to import the SQLAlchemy object.)
# 3. Ensure that the tables are created. (Models must be imported first.)
from vote import models
db.create_all()


# This has to happen after the DB is initialized and the tables are created,
# because the controller needs to query for the state of voting (open/closed).
from vote.controller import VoteController
api = VoteController(
    selection=app.config['SELECTION'],
    notification=app.config['NOTIFICATION'],
    winners=app.config['WINNERS'],
    premium_limit=app.config['PREMIUM_LIMIT']
)


# We can't import views until after the controller is initialized, because the
# behaviour is different depending on the state of voting.
from vote import views
