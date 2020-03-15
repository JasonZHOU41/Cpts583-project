# -*- coding: utf-8 -*-
from .models import User, Table, Menu, Order
from random import randint
from flask import flash, redirect, request
from flask import url_for
from myproject import db
import datetime
import json


def DoTask(task_id, table_id=None, order_id=None, employer_id=None):
    print("-------DoTask--------")
    print("Task id:", task_id)
    if task_id == 0:
        return AssignWaiter(table_id)
    if task_id == 1:
        print("Start order")
    if task_id == 2:  #  Complete order
        print("Kitchen has complete the order")
        return CompleteOrder(table_id, order_id)
    if task_id == 3:  #  Server complete, 用完餐了，结完账走人了
        return FinishOrder(table_id, employer_id)
    if task_id == 4:
        return CleanTable(table_id)


def AssignWaiter(table_id):
    print("-------------------AssignWaiter--------------")
    table = Table.query.filter_by(id=table_id).first()
    waiters = User.query.filter_by(role_id=1).all()
    free_waiters = []
    for waiter in waiters:
        if waiter.status != "busy":
            free_waiters.append(waiter)
    if free_waiters:
        index = randint(0, len(free_waiters))
        waiter = free_waiters[index]
        table.staff_id = waiter.id
        table.status = "Occupy"
        waiter.status = "busy"
        db.session.commit()
        return "waiter "+waiter.name+" is serving table "+str(table.id)
    else:
        return "There is no waiter free"


def CompleteOrder(table_id, order_id):
    print("-------------------Complete Order------------")
    table = Table.query.filter_by(id=table_id).first()
    order = Order.query.filter_by(id=order_id).first()
    order.status = "Ready"
    db.session.commit()
    waiter = User.query.filter_by(id=table.staff_id).first()
    return "Order for table "+str(table.id)+" has complete,\
    call waiter "+str(waiter.name)


def FinishOrder(table_id, employer_id):
    print("-------------------FinishOrder---------------")
    table = Table.query.filter_by(id=table_id).first()
    table.status = "Need Clean"
    table.order_id = None
    order = Order.query.filter_by(id=table.order_id).first()
    order.status = "Finish"
    order.table_id = 0
    employer = User.query.filter_by(id=employer_id).first()
    employer.status = "free"
    flash("Table "+str(table_id)+" has complete checkout")
    db.session.commit()
    CleanTable(table_id)


def CleanTable(table_id):
    print("-------------------CleanTable----------------")
    table = Table.query.filter_by(id=table_id).first()
    server = User.query.filter_by(id=table.staff_id).first()
    if server.role_id == 4:
        return "busboy"+server.name+"is cleaning table"+str(table.id)
    busboys = User.query.filter_by(role_id=4).all()
    free_busboys = []
    for busboy in busboys:
        if busboy.status != "busy":
            free_busboys.append(busboy)
    index = randint(0, len(free_busboys))
    busboy = free_busboys[index]
    table.staff_id = busboy.id
    busboy.status = "busy"
    db.session.commit()
    return "busboy "+busboy.name+" is cleaning table "+str(table.id)


def AddUser(form):
    if form.add_user.data and form.validate_on_submit():
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
        # print(user_username, user_pass, user_email, user_name, user_role)
        Users = User.query.filter_by(username=user_username).first()
        if Users:
            flash('User Already exits')
        else:
            new_user = User()
            new_user.username = user_username
            new_user.password = user_pass
            new_user.email = user_email
            new_user.name = user_name
            new_user.role_id = user_role
            new_user.status = "free"
            db.session.add(new_user)
            db.session.commit()
            flash("Success")
            return True


def AddMenu(form):
    if form.add.data and form.validate_on_submit():
        dish_name = form.name.data
        dish_price = form.price.data

        form.name.data = ''
        form.price.data = ''
        dish = Menu.query.filter_by(name=dish_name).first()
        if dish:
            flash('Already exits')
        else:
            new_dish = Menu()
            new_dish.name = dish_name
            new_dish.price = dish_price
            db.session.add(new_dish)
            db.session.commit()
            flash('success')
            return True


def AddOrder(table_id):
    order = Order()
    order.status = "Ordering"
    #order.time = datetime.datetime.now
    order.dishes = json.dumps([])
    order.table_id = table_id
    table = Table.query.filter_by(id=table_id).first()
    table.order_id = order.id
    db.session.add(order)
    db.session.commit()
    return order


def EditUser(form, target):
    form.id.data = str(target.id)
    form.username.data = target.username
    form.password.data = target.password
    form.email.data = target.email
    form.name.data = target.name
    form.role.data = str(target.role_id)

    if form.edit.data and form.validate_on_submit():
        target.username = request.form.get('username')
        target.password = request.form.get('password')
        target.email = request.form.get('email')
        target.name = request.form.get('name')
        target.role_id = request.form.get('role')
        # db.session.add(edit_user)
        db.session.commit()
        flash("Update successful!")
        return True


def DeleteMenu(form):
    if form.validate_on_submit():
        menu_id = request.form.get('id')
        print("---------------------------------------")
        print(menu_id)
        menu_list = Menu.query.filter_by(id=menu_id).first()
        db.session.delete(menu_list)
        db.session.commit()
        flash("delete success")
        return True

