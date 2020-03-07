# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect
from flask import g, url_for, request, session
from flask_login import login_user, login_required, current_user
from myproject import app, db, lm
from .forms import LoginForm
from .models import User


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


@app.after_login
def after_login(resp):
    if resp.name is None or resp.name == "":
        flash('Invalid login, please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(name=resp.name).first()
    if user is None:
        flash('User not exist!')
        return redirect(url_for('login'))
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="It's the index")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested')
        return redirect('/index')
    return render_template('login.html', title="Sign In", form=form)


@app.route('/Employee', methods=['GET', 'POST'])
@login_required
def employee():
    return render_template('employee.html', title="Employee")


@app.route('/employer/<nickname>', methods=['GET', 'POST'])
@login_required
def employer(nickname):
    return render_template('employer.html', title="Employer")


@app.route('/TableState', methods=['GET', 'POST'])
@login_required
def table():
    return render_template('table.html', title="Table")


@app.route('/Menu', methods=['GET', 'POST'])
@login_required
def menu():
    return render_template('menu.html', title="Menu")


@app.route('/OrderState', methods=['GET', 'POST'])
@login_required
def order():
    return render_template('order.html', title="Order")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
