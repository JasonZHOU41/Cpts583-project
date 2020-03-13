# -*- coding: utf-8 -*-


from flask import render_template, flash, redirect
from flask import g, url_for, request, session
from flask_login import login_user, login_required, current_user
from flask_login import logout_user
from myproject import app, db, lm
from .forms import *
from .models import *
from .utils import *


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
    role = request.args.get('role_name')
    name = request.args.get('user_name')
    print(role)
    print(name)
    if current_user.is_authenticated:
        role = Role.query.filter_by(id=current_user.role_id).first().name
        name = current_user.name
        return render_template('index.html',
                               title="It's the index current user activity",
                               role=role, name=name)
    return render_template('index.html', title="It's the index",
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
                # role_name = role.name.lower() if role.name == "Manager" else \
                #    "employer"
                return redirect(url_for(role.name.lower(), name=User_data.name))
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
    form = Add_Form()
    menu_add_form = Add_menu()
    edit_form = Edit_Form()
    table_list = Table.query.all()
    employer_list = User.query.all()
    menu_list = Menu.query.all()

    # Add User
    if AddUser(form):
        return redirect(url_for('manager', name=name))

    # Add menu item
    if AddMenu(menu_add_form):
        return redirect(url_for('manager', name=name))

    return render_template('manager.html', title="Manager", form=form,
                           table=table_list, employer=employer_list,
                           menu=menu_list, menu_add_form=menu_add_form,
                           edit_user=edit_form)


@app.route('/employer/<name>', methods=['GET', 'POST'])
@login_required
def employer(name):
    '''
        This page is for employers' personal information like salary,
        total work time, name, email or other things.
    '''
    print("Current user!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
    print(name)
    print(current_user.name)

    table_list = Table.query.all()
    return render_template('employer.html', title="Employer",
                           table=table_list)


'''
@app.route('/waiter/<name>')
@login_required
'''


@app.route('/host/<name>', methods=['GET', 'POST'])
@login_required
def host(name):
    table_list = Table.query.all()
    table_id = request.args.get("table_id")
    task_id = request.args.get("task_id")
    flash(DoTask(task_id, table_id))
    print('-----------------host---------------')
    print(table_id, task_id)
    return render_template('host.html', title="Host", table=table_list,
                           host_name=name)


'''
@app.route('/Kitchen/<name>', methods=['GET', 'POST'])
@login_required

@app.route('/Busboy/<name>', methods=['GET', 'POST'])
@login_required
'''


@app.route('/TableState', methods=['GET', 'POST'])
@login_required
def table():
    return render_template('table.html', title="Table")


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def menu():
    form = Edit_Form()
    user_id = request.args.get('user_id')
    where = request.args.get('from')
    # print("user is:", user)
    edit_user = User.query.filter_by(id=user_id).first()
    if form.edit.data and form.validate_on_submit():
        user_username = form.username.data
        user_pass = form.password.data
        user_email = form.email.data
        user_name = form.name.data
        user_role = form.role.data

        form.username.data = ''
        form.password.data = ''
        form.email.data = ''
        form.name.data = ''
        form.role.data = ''

        edit_user.username = user_username
        edit_user.password = user_pass
        edit_user.email = user_email
        edit_user.name = user_name
        edit_user.role_id = user_role
        db.session.commit()
        return redirect(url_for('manager', name=where))

    return render_template('menu.html', title="Menu", form=form,
                           edit_user=edit_user)


@app.route('/OrderState', methods=['GET', 'POST'])
@login_required
def order():
    table_id = request.args.get('table_id')
    print("----------------order------------------")
    print(table_id)
    menu = Menu.query.all()
    return render_template('order.html', title="Order", menu=menu)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    return render_template('index.html')
