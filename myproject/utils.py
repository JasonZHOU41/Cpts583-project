# -*- coding: utf-8 -*-
from .models import *


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
    return "Helloworld!"
    # for waiter in waiters:
        #  if waiter.status == '': # 如果有waiter空闲状态, 则分配
        #      waiter.status = ''
        #      table.status = ''
        #      return "waiter "+waiter.name+" is serving table "+table.id


def CleanTable(table_id):
    print("-------------------CleanTable----------------")
    table = Table.query.filter_by(id=table_id).first()
    ## call busboy to do the job.
    return "HelloHelloworld!"



