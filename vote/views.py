from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
import ldap3

from vote import app, db, lm, api
from vote.forms import LoginForm, VoteForm
from vote.models import User
from vote.authenticate import authenticate


@app.route('/')
@app.route('/index')
def index():
    if api.is_open:
        return redirect(url_for('ballot'))
    else:
        return redirect(url_for('results'))


@app.route('/ballot', methods=['GET', 'POST'])
@login_required
def ballot():
    user = g.user

    if not api.is_open:
        flash('Voting is currently closed.')
        return redirect(url_for('results'))

    form = VoteForm()

    if form.is_submitted():
        if form.validate_on_submit():
            ballot = form.ballot.data.split('|')
            if api.is_open:
                api.vote(user, *ballot)
            else:
                flash('Voting closed before your ballot was submitted.')
                return redirect(url_for('results'))

        else:
            flash('Unable to validate form: {}'.format(form.errors))

    if user.is_admin():
        admin_links = [
            ('Close', url_for('close')),
            ('Clear', url_for('clear')),
        ]
    else:
        admin_links = []

    return render_template(
        'vote.html', title='Vote', user=user, options=user.no_preferences,
        votes=user.preferences, form=form, admin_links=admin_links,
        voters=api.list_users(voted=True), info=app.config.get('INFO_TEXT')
    )


@app.route('/results')
@login_required
def results():
    user = g.user

    if user.is_admin():
        admin_links = [
            ('Close', url_for('close'))
                if api.is_open else ('Open', url_for('open')),
            ('Clear', url_for('clear')),
        ]
    else:
        admin_links = []

    return render_template(
        'results.html', title='Past Results' if api.is_open else 'Results',
        user=user, results=api.results(), admin_links=admin_links,
        info=app.config.get('INFO_TEXT')
    )


@app.route('/close')
@login_required
def close():
    user = g.user

    if user.is_admin():
        api.close()

    return redirect(url_for('index'))


@app.route('/open')
@login_required
def open():
    user = g.user

    if user.is_admin():
        api.open()

    return redirect(url_for('index'))


@app.route('/clear')
@login_required
def clear():
    user = g.user
    if user.is_admin():
        api.clear()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
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

        if user and user.is_authenticated:
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
