# -*- coding: utf-8 -*-
from .models import User, Table, Menu
from random import randint
from flask import flash, redirect
from flask import url_for
from myproject import db


def DoTask(task_id, table_id=None, order_id=None, employer_id=None):
    print("-------DoTask--------")
    print("Task id:", task_id)
    if task_id == 0:
        return AssignWaiter(table_id)
    if task_id == 1:
        print("Start order")
    if task_id == 2:
        print("Finish order")
        return FinishOrder(table_id, employer_id)
    if task_id == 3:
        return CleanTable(table_id)


def AssignWaiter(table_id):
    print("-------------------AssignWaiter--------------")
    table = Table.query.filter_by(id=table_id).first()
    waiters = User.query.filter_by(role_id=1).all()
    free_waiters = []
    for waiter in waiters:
        if waiter.status != "busy":
            free_waiters.append(waiter)
    index = randint(0, len(free_waiters))
    waiter = free_waiters[index]
    table.staff_id = waiter.id
    table.status = "Occupy"
    waiter.status = "busy"
    return "waiter "+waiter.name+" is serving table "+str(table.id)


def FinishOrder(table_id, employer_id):
    print("-------------------FinishOrder---------------")
    table = Table.query.filter_by(id=table_id).first()
    table.status = "Need Clean"
    employer = User.query.filter_by(id=employer_id).first()
    employer.status = "free"


def CleanTable(table_id):
    print("-------------------CleanTable----------------")
    table = Table.query.filter_by(id=table_id).first()
    busboys = User.query.filter_by(role_id=4).all()
    free_busboys = []
    for busboy in busboys:
        if busboy.status != "busy":
            free_busboys.append(busboy)
    index = randint(0, len(free_busboys))
    busboy = free_busboys[index]
    table.staff_id = busboy.id
    busboy.status = "busy"
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
