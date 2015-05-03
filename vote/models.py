from datetime import datetime

from vote import app, db


class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, index=True, unique=True)
    email = db.Column(db.String, index=True, unique=True)
    votes = db.relationship('Vote', backref='user', lazy='dynamic')
    history = db.relationship('History', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_admin(self):
        return self.id in app.config.get('ADMIN_USERS', [])

    def get_id(self):
        return self.id

    @property
    def voted(self):
        return self.votes.count() > 0

    @property
    def ballot(self):
        return [vote.option for vote in self.votes.order_by(Vote.rank).all()]

    @property
    def preferences(self):
        return [h.option for h in self.history.order_by(History.rank).all()]

    @property
    def no_votes(self):
        return [
            o for o in Option.query.order_by(Option.category).all()
            if o not in self.ballot
        ]

    @property
    def no_preferences(self):
        return [
            o for o in Option.query.order_by(Option.category).all()
            if o not in self.preferences
        ]


class Option(db.Model):
    name = db.Column(db.String, primary_key=True)
    category = db.Column(db.String, default=None)
    premium = db.Column(db.Boolean, default=False)
    added = db.Column(db.DateTime, default=datetime.utcnow)
    votes = db.relationship(
        'Vote', backref='option', lazy='dynamic', cascade='all'
    )
    history = db.relationship(
        'History', backref='option', lazy='dynamic', cascade='all'
    )
    results = db.relationship(
        'Results', backref='option', lazy='dynamic', cascade='all'
    )

    @property
    def new(self):
        highlight_new = app.config.get('HIGHLIGHT_NEW')

        if highlight_new is not None:
            return self.added + highlight_new > datetime.utcnow()
        else:
            return False

    def __repr__(self):
        return '<Option {}>'.format(self.name)


class Vote(db.Model):
    rank = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    option_id = db.Column(
        db.String, db.ForeignKey('option.name'), primary_key=True
    )

    def __repr__(self):
        return '<Vote {}: {}>'.format(self.option.name, self.rank)


class History(db.Model):
    rank = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    option_id = db.Column(
        db.String, db.ForeignKey('option.name'), primary_key=True
    )

    def __repr__(self):
        return '<History {}: {}>'.format(self.option.name, self.rank)


class Results(db.Model):
    rank = db.Column(db.Integer)
    option_id = db.Column(
        db.String, db.ForeignKey('option.name'), primary_key=True
    )

    def __repr__(self):
        return '<Results {}: {}>'.format(self.option.name, self.rank)


class State(db.Model):
    is_open = db.Column(db.Boolean, default=True, primary_key=True)

    def __repr__(self):
        return '<State {}>'.format('Open' if self.is_open else 'Closed')
