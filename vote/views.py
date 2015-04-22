from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
import ldap3

from vote import app, db, lm, api
from vote.forms import LoginForm
#from vote.models import User, Option, Vote # Should never need this. Use API.
from vote.authenticate import authenticate


SELECTION = app.config['SELECTION']


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('ballot'))


@app.route('/ballot')
@login_required
def ballot():
    user = g.user

    if user.voted:
        return redirect(url_for('results'))

    # Create the ballot and stuff.

    return render_template('base.html', user=user, title='Ballot')


@app.route('/results')
@login_required
def results():
    user = g.user

    # Display the user's ballot, along with the current "best" ballot? (Is this
    # possible with multiple "pick the winner" algorithms? I guess each would
    # have to define a way to view the ballot, too?)

    return render_template('base.html', user=user, title='Results')



### OLD STUFF FROM LUNCH VOTER. TO BE COMPLETELY REWRITTEN.
"""


@app.route('/<type>', methods=['GET', 'POST'])
@login_required
def vote(type):
    user = g.user

    if type not in TYPES:
        flash('Unknown type: "{}".'.format(type))
        return redirect(url_for("index"))

    toggle = TYPES[(TYPES.index(type) + 1) % len(TYPES)]
    options = OPTIONS[type]
    premium = PREMIUM[type]

    title = "{} Day Voter!".format(type.capitalize())

    votes = User.query.get(user.id).votes.filter_by(type=type).all()
    favourites = User.query.get(user.id).favourites.filter_by(type=type).all()

    # Define categories (if options are divided into categories).
    categories = None
    if isinstance(options, dict):
        categories = options
        options = [item for cat in categories for item in categories[cat]]

    form = create_ballot(type, options, user)

    if form.is_submitted():
        print('Form submitted. Validating...')

        if form.validate_on_submit():
            print('Validated ballot: {}'.format(form))
            submit_vote(type, options, user, form)
            return redirect(url_for("vote", type=type))

        else:
            print('Unable to validate: {}'.format(form.errors))
 
    winners = []
    if votes:
        if WEEKLY_MODE:
            if BIWEEKLY:
                winners = biweekly_winners(type)
            else:
                winners = weekly_winners(type)

        else:
            winners = determine_winners(type, RUNNERS_UP + 1)

    if categories:
        template = "complex_ballot.html"
        options = categories
    else:
        template = "simple_ballot.html"

    voters = list(filter(lambda u: u.votes.filter_by(type=type).all(),
                  User.query.all()))
    return render_template(template, title=title, user=user, type=type,
                           options=options, premium=premium, form=form,
                           winner=winners, weekly=WEEKLY_MODE, voters=voters,
                           toggle=toggle)


@app.route('/<type>/history')
@login_required
def show_history(type):
    title = "{} Voting History".format(type.capitalize())
    options = OPTIONS[type]
    if isinstance(options, dict):
        categories = options
        options = [item for cat in categories for item in categories[cat]]

    return render_template("history.html", title=title, user=g.user, type=type,
                           history=history(type, options),
                           premium=PREMIUM[type])


@app.route('/<type>/close')
@login_required
def close(type):
    user = g.user
    if user.is_admin():
        close_votes(type)
    return redirect(url_for('index'))


@app.route('/clear')
@login_required
def clear():
    user = g.user
    if user.is_admin():
        clear_votes()
    return redirect(url_for('index'))


@app.route('/clear_preferences')
@login_required
def clear_preferences():
    user = g.user
    clear_favourites(user)
    return redirect(url_for('index'))
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', title="Log In", form=form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        print('Logging in...')
        user = authenticate(username, password)

        if not user:
            print('Login failed.')
            flash('Login failed.')
            return render_template('login.html', title="Log In", form=form)

        if user and user.is_authenticated():
            db_user = User.query.get(user.id)
            if db_user is None:
                db.session.add(user)
                db.session.commit()

            login_user(user, remember=form.remember.data)

            return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', title="Log In", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@lm.user_loader
def load_user(id):
    return User.query.get(id)


@app.before_request
def before_request():
    g.user = current_user
