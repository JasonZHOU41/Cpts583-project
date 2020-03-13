# -*- coding: utf-8 -*-
from .models import *


def DoTask(task_id, table_id, order_id=None, employer_id=None):
    print("Task id:", task_id)
    if task_id == '0':
        AssignWaiter(table_id)
    if task_id == '1':
        print("Start order")
    if task_id == '2':
        print("Finish order")
    if task_id == '3':
        print("Clean table")


def AssignWaiter(table_id):
    u = User.query.filter_by(role_id='1').all()
    print("-------------------AssignWaiter--------------")
    print(u)



