# -*- coding: utf-8 -*-


from myproject import db
from flask import current_app
from flask_login import UserMixin
import datetime


class Role(db.Model):
    __tablename__ = "roles"
    # id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)  # 主键自增，唯一，不可为空
    name = db.Column(db.String(32), unique=True)

    def __repr__(self):
        return "Role object: name=%s" % self.name


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)  # 主键自增，唯一，不可为空
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(64), nullable=False)  # 员工名字
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer)  #
    status = db.Column(db.String(64), nullable=False)

    '''
    id- name
    1- Waiter
    2- Host
    3- Kitchen
    4- Busboy
    5- Manager
    '''

    def __repr__(self):
        return "User object: name=%s" % self.name

    # @staticmethod
    # def init_admin():
    #     db.drop_all()
    #     db.create_all()
    #     u1 = User()
    #     u1.username = "admin"
    #     u1.password = "111222"
    #     u1.name = 'BOb'
    #     u1.email = "350342629@qq.com"
    #     u1.role_id = '1'
    #     u1.status = 'free'
    #     db.session.add(u1)
    #     db.session.commit()


class Table(db.Model):
    __tablename__ = "table"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)  # 主键自增，唯一，不可为空
    # status = db.Column(db.Integer, db.ForeignKey("table_status.id"), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # new!!!
    status = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return "Table object: id=%s" % self.id


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


class Detail(db.Model):
    __tablename__ = "detail"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)  # 主键自增，唯一，不可为空
    dish_id = db.Column(db.Integer, db.ForeignKey("menu.id"), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Detail object: name=%s" % self.name
