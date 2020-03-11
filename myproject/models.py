# -*- coding: utf-8 -*-

from myproject import db
from flask import current_app


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    # id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)  # 主键自增，唯一，不可为空
    name = db.Column(db.String(32), unique=True)

    def __repr__(self):
        return "Role object: name=%s" % self.name


class User(db.Model):
    __tablename__ = "users"
    # id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)  # 主键自增，唯一，不可为空
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    name = db.Column(db.String(64), nullable=False)  # 员工名字
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, unique=True)

    def __repr__(self):
        return "User object: name=%s" % self.name

    # @staticmethod
    # def init_admin():
    #     db.drop_all()
    #     db.create_all()
    #     u1 = User()
    #     u1.name = "Admin"
    #     u1.password = "Admin_Password"
    #     u1.email = "350535629@qq.com"
    #     db.session.add(u1)
    #     db.session.commit()

class Table(db.Model):
    __tablename__ = "table"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)  # 主键自增，唯一，不可为空
    status = db.Column(db.Integer, db.ForeignKey("table_status.id"), nullable=False)

    def __repr__(self):
        return "Table object: name=%s" % self.name


class Table_status(db.Model):
    __tablename__ = "table_status"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)  # 主键自增，唯一，不可为空
    status = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return "Table_status object: name=%s" % self.name


class Menu(db.Model):
    __tablename__ = "menu"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)  # 主键自增，唯一，不可为空
    name = db.Column(db.String(64), unique=True)
    price = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return "Menu object: name=%s" % self.name


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)  # 主键自增，唯一，不可为空
    status = db.Column(db.Boolean, nullable=False)
    income = db.Column(db.String(64), nullable=False)
    # dishes_id = db.Column(db.Integer, db.ForeignKey("menu.id"))

    def __repr__(self):
        return "Order object: name=%s" % self.name
