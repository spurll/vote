from vote import app, db
from vote.models import User, Option, Vote
from vote.selection import instant_runoff


class VoteController(object):
    def __init__(self, selection=instant_runoff):
        self.selection = selection

    def vote(self):
        pass

    def results(self):
        pass

    def clear(self):
        pass

    def add(self, name, category=None, premium=False):
        """
        Adds a new Option to the database.
        """
        o = Option(name=name, category=category, premium=premium)
        db.session.add(o)
        db.session.commit()

    def categorize(self, name, category):
        """
        Changes the category of an Option in the database.
        """
        o = Option.query.filter(Option.name == name).one()
        o.category = category
        db.session.add(o)
        db.session.commit()

    def list(self):
        """
        Returns a dict with categories as the keys and options as the values.
        """
        listing = {}

        for o in Option.query.all():
            listing[o.category] = listing.get(o.category, []) + [o.name]

        return listing
