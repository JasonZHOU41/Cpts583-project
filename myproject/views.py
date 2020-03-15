# -*- coding: utf-8 -*-


from flask import render_template, flash, redirect
from flask import g, url_for, request, session
from flask_login import login_user, login_required, current_user
from flask_login import logout_user
from myproject import app, db, lm
from .forms import *
from .models import Role, User, Table, Menu, Order, Detail
from .utils import *
import json


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


@app.route('/manager/<name>', methods=['GET', 'POST'])
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


@app.route('/waiter/<name>')
@login_required
def waiter(name):
    waiter_id = User.query.filter_by(name=name).first().id
    table_list = Table.query.filter_by(staff_id=waiter_id).all()
    table_id = request.args.get("table_id")
    task_id = request.args.get("task_id")
    order_id = request.args.get("order_id")
    if order_id:
        order = Order.query.filter_by(id=order_id).first()
        order.status = "Prepare"
        db.session.commit()
    if task_id and table_id:
        task_id = int(task_id)
        if task_id == 3:
            flash(DoTask(task_id, table_id, order_id=None,
                         employer_id=waiter_id))
        if task_id == 5:
            order = Order.query.filter_by(table_id=table_id).first()
            if order is None:
                order = AddOrder(table_id)
            return redirect(url_for("order", order_id=order.id,
                                    table_id=table_id, waiter_id=waiter_id))
    return render_template('waiter.html', title="Waiter",
                           table=table_list, waiter_name=name)


@app.route('/host/<name>', methods=['GET', 'POST'])
@login_required
def host(name):
    table_list = Table.query.all()
    table_id = request.args.get("table_id")
    task_id = request.args.get("task_id")
    if table_id:
        print("-----Start do work--------")
        print(table_id)
        table = Table.query.filter_by(id=table_id).first()
        if table.status == "Available":  # if table available, call waiter
            flash(DoTask(0, table_id))
        elif table.status == "Need Clean":  # if table needs clean, call busboy
            flash(DoTask(4, table_id))
        else:
            pass
    print('-----------------host---------------')
    print(table_id, task_id)
    return render_template('host.html', title="Host", table=table_list,
                           host_name=name)


@app.route('/kitchen/<name>', methods=['GET', 'POST'])
@login_required
def kitchen(name):
    order_list = Order.query.filter_by(status="Prepare").all()
    order_id = request.args.get("order_id")
    table_id = request.args.get("table_id")
    if order_id and table_id:
        print('---------------try-----finish order!----------')
        flash(DoTask(task_id=2, table_id=table_id, order_id=order_id))
    print('----------------kitchen-------------')
    return render_template('kitchen.html', title="Kitchen", orders=order_list,
                           kitchen_name=name)


@app.route('/busboy/<name>', methods=['GET', 'POST'])
@login_required
def busboy(name):
    busboy = User.query.filter_by(name=name).first()
    busboy_id = busboy.id
    table_list = Table.query.filter_by(staff_id=busboy_id).all()
    table_id = request.args.get("table_id")
    if table_id:
        busboy.status = "free"
        table = Table.query.filter_by(id=table_id).first()
        table.status = "Available"
        table.staff_id = None
        db.session.commit()
        flash("Table "+str(table_id)+" has been cleaned")
    return render_template('busboy.html', title="Busboy", table=table_list,
                           busboy_name=name)


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
    edit_user = User.query.filter_by(id=user_id).first()

    if EditUser(form, edit_user):
        return redirect(url_for('manager', name=where))

    return render_template('menu.html', title="Menu", form=form,
                           user_id=user_id, where=where, edit_user=edit_user)


@app.route('/OrderState', methods=['GET', 'POST'])
@login_required
def order():
    table_id = request.args.get('table_id')
    order_id = request.args.get('order_id')
    waiter_id = request.args.get('waiter_id')
    delete = request.args.get('delete')
    order = Order.query.filter_by(id=order_id).first()
    dish_list = []
    if order:
        dishes = json.loads(order.dishes)
        for dish_id in dishes:
            dish_list.append(Menu.query.filter_by(id=dish_id).first())
    print("----------------order------------------")
    print(table_id)
    print(order_id)
    menu = Menu.query.all()

    print("----------------AddOrder---------------")
    dish_id = request.args.get('dish_id')
    if dish_id and order:
        if delete:
            dishes.remove(dish_id)
            order.dishes = json.dumps(dishes)
            db.session.commit()
        else:
            dishes.append(dish_id)
            order.dishes = json.dumps(dishes)
            db.session.commit()
    #refresh = request.args.get()
    return render_template('order.html', title="Order", menu=menu,
                order_id=order_id, dishes=dish_list, waiter_id=waiter_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    return render_template('index.html')
