from os import urandom, path, environ
from datetime import timedelta
from functools import partial

from vote.selection import weighted_sample
from vote.notification import slack, email


# Web Server
CSRF_ENABLED = True
SECRET_KEY = urandom(30)
PROPAGATE_EXCEPTIONS = True
REMEMBER_COOKIE_NAME = 'vote_token'     # Needs to be unique server-wide.

# SQLAlchemy
basedir = path.abspath(path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(path.join(basedir, 'app.db'))

# LDAP
LDAP_URI = 'ldap://YOUR.LDAP.URI'
LDAP_SEARCH_BASE = 'ou=????,dc=????,dc=????'

# Administrator
ADMIN_USERS = ['LDAP.USER.ID.HERE']

# Voting
WINNERS = 5             # 5 options will be selected.
PREMIUM_LIMIT = 2       # No more than 2 "premium" options will be selected.
SELECTION = weighted_sample

# Display
HIGHLIGHT_NEW = timedelta(days=7)
INFO_TEXT = (
    'Drag any number of options from the column on the left into your ballot '
    'on the right and sort in order of preference. Here is a link to '
    '<a href="LINK_HERE">more information</a>.'
)

# Slack
SLACK_TOKEN = environ.get('SLACK_TOKEN')
SLACK_USER = 'VoteBot'
SLACK_ICON = 'http://LINK.TO.BOT.IMAGE'
SLACK_RECIPIENT = '#CHANNEL'
SLACK_ADDENDUM = 'Any additional information you want in the message.'

# Email
EMAIL_HOST = 'smtp.gmail.com:587'
EMAIL_USER = 'YOUR.EMAIL@gmail.com'
EMAIL_PASSWORD = 'YOUR_APPLICATION_SPECIFIC_PASSWORD'
EMAIL_RECIPIENTS = ['RECIPIENT.1@gmail.com', 'RECIPIENT.2@gmail.com']
EMAIL_ADDENDUM = 'Any additional information you want in the message.'

# Notification
NOTIFICATION = partial(
    slack, token=SLACK_TOKEN, user=SLACK_USER, icon=SLACK_ICON,
    recipient=SLACK_RECIPIENT, addendum=SLACK_ADDENDUM
)

#NOTIFICATION = partial(
#    email, host=EMAIL_HOST, user=EMAIL_USER, password=EMAIL_PASSWORD,
#    recipients=EMAIL_RECIPIENTS, addendum=EMAIL_ADDENDUM
#)
