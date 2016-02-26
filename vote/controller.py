import csv, re

from vote import app, db
from vote.models import User, Option, Vote, Results, History, State
from vote.selection import instant_runoff


class VoteController(object):
    def __init__(
        self,
        selection=None,
        notification=None,
        winners=None,
        premium_limit=None
    ):
        if selection is None:
            selection = instant_runoff

        if winners is None:
            winners = 1

        self.selection = selection
        self.notification = notification
        self.winners = winners
        self.premium_limit = premium_limit

        if State.query.count() < 1:
            s = State(is_open=True)

            try:
                db.session.add(s)
                db.session.commit()
            except:
                db.session.rollback()
                raise

    @property
    def is_open(self):
        return State.query.one().is_open

    def vote(self, user, *args):
        """
        Casts a ballot (what we call a series of ranked votes) for a series of
        options, in the order specified.
        """
        if not self.is_open:
            raise Exception('Voting is closed.')

        if len(args) != len(set(args)):
            raise Exception('Votes must be unique.')

        try:
            # Delete user's votes and history first.
            user.votes.delete()
            user.history.delete()
            db.session.commit()
        except:
            db.sesion.rollback()
            raise

        for index, option in enumerate(args):
            rank = index + 1        # First choice is #1, then #2, etc.
            try:
                o = Option.query.filter(Option.name == option).one()
            except:
                # Sometimes (most of the time) the category will also be
                # included. This is a terribly lazy way to handle this, Gem.
                option = re.sub(' \(.*\)$', '', option)
                o = Option.query.filter(Option.name == option).one()

            # Create vote and history objects. (History is used to re-populate
            # new ballots with old votes, to save the user time in subsequent
            # rounds of voting. It's kind of a hack.)
            v = Vote(rank=rank)
            h = History(rank=rank)

            # Associate the vote and history objects with the option and user.
            o.votes.append(v)
            o.history.append(h)
            user.votes.append(v)
            user.history.append(h)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def results(self):
        """
        Retrieves the results in the form of Option objects from the database.
        """
        return [r.option for r in Results.query.order_by(Results.rank).all()]

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
        Determins the winner(s), based on the selection algorithm provided at
        initialization, saves this information to the database, issues the
        appropriate notification (if any), and then clears votes, returning the
        results.
        """
        if not self.is_open:
            raise Exception('Voting is already closed.')

        # Get results.
        results = self.selection(
            self.list_votes(), self.winners, self.premium_limit,
        )

        # Clear the Results table.
        try:
            Results.query.delete()
            db.session.commit()
        except:
            db.session.rollback()
            raise

        # Update the Results table.
        for index, o in enumerate(results):
            r = Results(rank=index + 1)
            o.results.append(r)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

        # Delete votes and close voting.
        self.clear()

        State.query.one().is_open = False;
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

        # Notify.
        self.notify()

        return results

    def open(self):
        """
        Opens the voting session, which allows votes to be cast.
        """
        if self.is_open:
            raise Exception('Voting is already open.')

        State.query.one().is_open = True;
        try:
            db.session.commit()
        except:
            db.session.rollback()
            raise

    def change_option(self, name, category=None, premium=None):
        """
        Changes the category or premiumness of an option in the database.
        """
        o = Option.query.filter(Option.name == name).one()

        if category is not None:
            o.category = category

        if premium is not None:
            o.premium = premium

        try:
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

    def import_options(self, file_name):
        """
        Imports a list of options into the database from a CSV file. This file
        should have the following format: name, category, premium (True/False)
        """
        with open(file_name) as file:
            reader = csv.reader(file)
            for row in reader:
                option = {
                    'name': row[0] if row else None,
                    'category': row[1] if len(row) > 1 else None,
                    'premium': row[2] if len(row) > 2 else False
                }

                if option['name']:
                    print('Adding new option: {}'.format(option['name']))
                    o = Option(**option)

                    try:
                        db.session.add(o)
                        db.session.commit()
                    except Exception as e:
                        db.session.rollback()
                        print (
                            'Unable to add {} to the database: {}'
                            .format(option['name'], e)
                        )

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

    def delete_option(self, name):
        """
        Removes an option to the database.
        """
        try:
            Option.query.filter(Option.name == name).delete()
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
                listing[o.category] = listing.get(o.category, []) + [o]

        return listing

    def list_users(self, voted=None):
        """
        Returns a list of all users. If voted is set to True or False, only
        return a list of users who have (or have not) voted.
        """
        if voted is None:
            return User.query.all()
        else:
            return [u for u in User.query.all() if u.voted == voted]

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
