# -*- coding: utf-8 -*-


from myproject import db
from flask import current_app
from flask_login import UserMixin
import datetime


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True,
                   nullable=False)  # 主键自增，唯一，不可为空
    name = db.Column(db.String(32), unique=True)

    def __repr__(self):
        return "Role object: name=%s" % self.name

    '''
    id- name
    1- Waiter
    2- Host
    3- Kitchen
    4- Busboy
    5- Manager
    '''


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True,
                   nullable=False)  # 主键自增，唯一，不可为空
    username = db.Column(db.String(64), unique=True)  # The name for login
    email = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(64), nullable=False)  # 员工名字
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer)
    status = db.Column(db.String(64), nullable=False)  # busy/free

    def __repr__(self):
        return "User object: name=%s" % self.name


class Table(db.Model):
    __tablename__ = "table"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True,
                   nullable=False)  # 主键自增，唯一，不可为空
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    status = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return "Table object: id=%s" % self.id

    '''
    Table - 3 status:
    1. Available
    2. Occupy
    3. Need Clean
    '''


class Menu(db.Model):
    __tablename__ = "menu"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)  # 主键自增，唯一，不可为空
    name = db.Column(db.String(128), unique=True)
    price = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return "Menu object: name=%s" % self.name


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)  # 主键自增，唯一，不可为空
    status = db.Column(db.String(64), nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)

    def __repr__(self):
        return "Order object: name=%s" % self.name

    '''
    Order - 3 status
    1. Prepare: Initial status of the order(When waiter click the order button)
        - Click "Order" button, check the order is exits or not,
            if yes, show the order detail.

            else, set a new Order record on the "order" table.
                  Fill the order_id on the "table" table
                  When add a dish from menu, opera the "detail" table

    2. Ready: When kitchen finish the order(ignore the single dish)
        - Change the order status

    3. Finish: When waiter click the "Finish order" button
        - Clean the order_id on the "table" table
    '''


class Detail(db.Model):
    __tablename__ = "detail"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)  # 主键自增，唯一，不可为空
    dish_id = db.Column(db.Integer, db.ForeignKey("menu.id"), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Detail object: name=%s" % self.name
