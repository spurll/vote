from vote import app, db
from vote.models import User, Option, Vote
from vote.selection import instant_runoff


class VoteController(object):
    def __init__(
        self,
        selection=instant_runoff,
        notification=None,
        winners=1,
        premium_limit=None
    ):
        self.selection = selection
        self.notification = notification
        self.winners = winners
        self.premium_limit = premium_limit

    def vote(self, user, *args):
        """
        Casts a ballot (what we call a series of ranked votes) for a series of
        options, in the order specified.
        """
        if user.voted:
            raise Exception('User {} has already voted.'.format(user.id))

        if len(args) != len(set(args)):
            raise Exception('Votes must be unique.')

        for index, option in enumerate(args):
            rank = index + 1        # First choice is #1, then #2, etc.
            v = Vote(rank=rank)
            o = Option.query.filter(Option.name == option).one()
            o.votes.append(v)
            user.votes.append(v)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def results(self):
        """
        Determins the winner(s), based on the selection algorithm provided at
        initialization.
        """
        return self.selection(self.list_votes(), self.winners)

    def notify(self):
        """
        Notifies users of the results of the vote, using the notification
        function provided on initialization.
        """
        if self.notification:
            self.notification(self.results())

    def clear(self, user=None):
        """
        If a user is provided, removes the specified user's votes from the
        database. Otherwise, removes all votes from the database.
        """
        try:
            if user:
                # Delete the specified user's votes.
                user.votes.delete()
            else:
                # Delete all votes.
                Vote.query.delete()

            db.session.commit()
        except:
            db.session.rollback()
            raise

    def close(self):
        """
        Gets the final results, issues the appropriate notification (if any),
        and then clears votes. Returns the results before clearing.
        """
        results = self.results()

        if self.notify:
            self.notify(results)

        self.clear()

        return results

    def change_category(self, name, category):
        """
        Changes the category of an option in the database.
        """
        o = Option.query.filter(Option.name == name).one()
        o.category = category

        try:
            db.session.add(o)
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def add_option(self, name, category=None, premium=False):
        """
        Adds a new option to the database.
        """
        o = Option(name=name, category=category, premium=premium)

        try:
            db.session.add(o)
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def add_user(self, user_id, name, email):
        """
        Adds a new user to the database.
        """
        u = User(id=user_id, name=name, email=email)

        try:
            db.session.add(u)
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def list_options(self, as_dict=False):
        """
        Returns a list of all options. If as_dict is True, instead returns a
        dict with the categories as keys and the option names as the values.
        """
        if not as_dict:
            listing = Option.query.order_by(Option.category).all()
        else:
            listing = {}

            for o in Option.query.all():
                listing[o.category] = listing.get(o.category, []) + [o.name]

        return listing

    def list_users(self):
        """
        Returns a list of all users.
        """
        return User.query.all()

    def list_votes(self, user=None, as_dict=False):
        """
        If a user is provided, returns a list of the specified user's votes (as
        Option objects, not Vote objects). Otherwise, returns a dict with
        usernames as keys and lists of votes (Options) as values.
        """
        if user:
            # List the specified user's votes.
            v = user.ballot
        else:
            # List all votes.
            if as_dict:
                v = {u.id: u.ballot for u in User.query.all()}
            else:
                v = [u.ballot for u in User.query.all()]

        return v
