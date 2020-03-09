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


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="It's the index")


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
        Create function for login, check user info
        within database
    '''
    form = LoginForm()
    User.init_admin()

    if form.validate_on_submit():
        # uname = form.username.data
        input_name = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(name=input_name).first()
        if user is None:
            flash("user does not exits")
        else:
            # if user.password == form.password.data:
            if user.password == password:
                print('User info:', user)
                flash('Login successful')
                return redirect('/index')
            else:
                flash('Wrong password')
    return render_template('login.html', title="Sign In", form=form)


@app.route('/Employee', methods=['GET', 'POST'])
@login_required
def employee():
    '''
        Manager's website
        need check authority.
        need show information about all employers
        need show income of the restaurant
    '''
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
@login_required
def logout():
    #logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    return render_template('index.html')
