from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
import ldap3

from vote import app, db, lm
from vote.forms import LoginForm, VoteForm
from vote.models import User
from vote.authenticate import authenticate
from vote.controller import VoteController


selection = app.config.get('SELECTION')
notification = app.config.get('NOTIFICATION')
winners = app.config.get('WINNERS')
premium = app.config.get('PREMIUM_LIMIT')


@app.route('/')
@app.route('/index')
def index():
    api = VoteController(selection=selection, notification=notification,
        winners=winners, premium_limit=premium)

    if api.is_open:
        return redirect(url_for('ballot'))
    else:
        return redirect(url_for('results'))


@app.route('/ballot', methods=['GET', 'POST'])
@login_required
def ballot():
    api = VoteController(selection=selection, notification=notification,
        winners=winners, premium_limit=premium)

    if not api.is_open:
        flash('Voting is currently closed.')
        return redirect(url_for('results'))

    form = VoteForm()

    if form.is_submitted():
        if form.validate_on_submit():
            ballot = form.ballot.data.split('|')
            if api.is_open:
                api.vote(g.user, *ballot)
            else:
                flash('Voting closed before your ballot was submitted.')
                return redirect(url_for('results'))

        else:
            flash_errors(form)

    if g.user.is_admin():
        admin_links = [
            ('Close Voting', url_for('close')),
            ('Burn Ballots', url_for('clear')),
        ]
    else:
        admin_links = []

    return render_template(
        'vote.html',
        title='Vote',
        user=g.user,
        options=g.user.no_preferences,
        votes=g.user.preferences,
        form=form,
        admin_links=admin_links,
        voters=api.list_users(voted=True),
        info=app.config.get('INFO_TEXT')
    )


@app.route('/results')
@login_required
def results():
    api = VoteController(selection=selection, notification=notification,
        winners=winners, premium_limit=premium)

    if g.user.is_admin():
        admin_links = [
            ('Close Voting', url_for('close'))
                if api.is_open else ('Open Voting', url_for('open')),
            ('Burn Ballots', url_for('clear')),
        ]
    else:
        admin_links = []

    return render_template(
        'results.html',
        title='Past Results' if api.is_open else 'Results',
        user=g.user,
        results=api.results(),
        admin_links=admin_links,
        info=app.config.get('INFO_TEXT')
    )


@app.route('/close')
@login_required
def close():
    api = VoteController(selection=selection, notification=notification,
        winners=winners, premium_limit=premium)

    if g.user.is_admin():
        api.close()

    return redirect(url_for('index'))


@app.route('/open')
@login_required
def open():
    api = VoteController(selection=selection, notification=notification,
        winners=winners, premium_limit=premium)

    if g.user.is_admin():
        api.open()

    return redirect(url_for('index'))


@app.route('/clear')
@login_required
def clear():
    api = VoteController(selection=selection, notification=notification,
        winners=winners, premium_limit=premium)

    if g.user.is_admin():
        api.clear()

    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', title='Log In', form=form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user, message = authenticate(username, password)

        if not user:
            flash('Login failed: {}'.format(message))
            return render_template('login.html', title='Log In', form=form)

        if user and user.is_authenticated:
            db_user = User.query.get(user.id)
            if db_user is None:
                db.session.add(user)
                db.session.commit()

            login_user(user, remember=form.remember.data)

            return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', title='Log In', form=form)


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


def flash_errors(form):
    for field, messages in form.errors.items():
        label = getattr(getattr(getattr(form, field), 'label'), 'text', '')
        label = label.replace(':', '')
        error = ', '.join(messages)

        message = f'Error in {label}: {error}' if label else 'Error: {error}'

        flash(message)
        print(message)
