# -*- coding: utf-8 -*-
from .models import *
from flask import flash, redirect
from flask import url_for


def DoTask(task_id, table_id=None, order_id=None, employer_id=None):
    print("Task id:", task_id)
    if task_id == '0':
        return AssignWaiter(table_id)
    if task_id == '1':
        print("Start order")
    if task_id == '2':
        print("Finish order")
    if task_id == '3':
        CleanTable(table_id)


def AssignWaiter(table_id):
    print("-------------------AssignWaiter--------------")
    waiters = User.query.filter_by(role_id='1').all()
    table = Table.query.filter_by(id=table_id).first()
    return "Hello world!"
    # for waiter in waiters:
    #  if waiter.status == '': # 如果有waiter空闲状态, 则分配
    #      waiter.status = ''
    #      table.status = ''
    #      return "waiter "+waiter.name+" is serving table "+table.id


def CleanTable(table_id):
    print("-------------------CleanTable----------------")
    table = Table.query.filter_by(id=table_id).first()
    # call busboy to do the job.
    return "Hello Hello world!"


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
