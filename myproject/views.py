# -*- coding: utf-8 -*-


from flask import render_template, flash, redirect
from flask import g, url_for, request, session
from flask_login import login_user, login_required, current_user
from flask_login import logout_user
from myproject import app, db, lm
from .forms import LoginForm, Add_Form
from .models import User, Role


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    # if not session.get('user'):
    #    return redirect(url_for('login'))
    pass


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = Add_Form()  # Test the add form
    role = request.args.get('role_name')
    name = request.args.get('user_name')
    print(role)
    print(name)
    if current_user.is_authenticated:
        role = Role.query.filter_by(id=current_user.role_id).first().name
        name = current_user.name
        return render_template('index.html',
                               title="It's the indexcurrent user activity",
                               form=form, role=role, name=name)
    return render_template('index.html', title="It's the index", form=form,
                           role=role, name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
        Create function for login, check user info
        within database
    '''
    form = LoginForm()

    if form.validate_on_submit():
        input_name = form.username.data
        password = form.password.data
        User_data = User.query.filter_by(username=input_name,
                                         password=password).first()
        if User_data is None:
            flash("user does not exits or wrong password")
        else:
            role = Role.query.filter_by(id=User_data.role_id).first()
            if User_data.password == password:
                print('User info:', User_data, 'password:', User_data.password)
                login_user(User_data)
                flash('Login successful')
                role_name = role.name.lower() if role.name == "Manager" else\
                    "employer"
                return redirect(url_for(role_name, name=User_data.name))
                #  return redirect(url_for('index', role_name=role.name,
                #                        user_name=User_data.username))
            else:
                flash('Wrong password')
    return render_template('login.html', title="Sign In", form=form)


@app.route('/Manager/<name>', methods=['GET', 'POST'])
@login_required
def manager(name):
    '''
        Manager's website
        need check authority.
        need show information about all employers
        need show income of the restaurant
    '''
    print("Current Manager!!!!!!!!!!!!!!!!!!!!!!!!!!!11")
    print(name)
    print(current_user.name)
    return render_template('manager.html', title="Manager")


@app.route('/employer/<name>', methods=['GET', 'POST'])
@login_required
def employer(nickname):
    '''
        This page is for employers' personal information like salary,
        total work time, name, email or other things.
    '''
    print("Current user!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
    print(current_user.name)
    return render_template('employer.html', title="Employer")


'''
@app.route('/Waiter/<name>')
@login_required

@app.route('/Host/<name>', methods=['GET', 'POST'])
@login_required

@app.route('/Kitchen/<name>', methods=['GET', 'POST'])
@login_required

@app.route('/Busboy/<name>', methods=['GET', 'POST'])
@login_required
'''


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
    logout_user()
    return redirect(url_for('login'))


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    return render_template('index.html')
