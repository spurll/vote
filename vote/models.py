from datetime import datetime

from vote import app, db


class User(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    votes = db.relationship('Vote', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.id in app.config['ADMIN_USERS']

    def get_id(self):
        return self.id

    @property
    def voted(self):
        return self.votes.count() > 0

    @property
    def ballot(self):
        return [vote.option for vote in self.votes.order_by(Vote.rank).all()]


class Option(db.Model):
    name = db.Column(db.String(128), primary_key=True)
    category = db.Column(db.String(128), default=None)
    premium = db.Column(db.Boolean, default=False)
    added = db.Column(db.DateTime, default=datetime.utcnow)
    votes = db.relationship('Vote', backref='option', lazy='dynamic')

    @property
    def new(self):
        return self.added + app.config['HIGHLIGHT_NEW'] > datetime.utcnow()

    def __repr__(self):
        return '<Option {}>'.format(self.name)


class Vote(db.Model):
    rank = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    option_id = db.Column(db.Integer, db.ForeignKey('option.name'),
                          primary_key=True)

    def __repr__(self):
        return '<Vote {}: {}>'.format(self.option.name, self.rank)
