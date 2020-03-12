# -*- coding: utf-8 -*-


from myproject import db
from flask import current_app
from flask_login import UserMixin


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
    role_id = db.Column(db.Integer)
    status = db.Column(db.String(64), nullable=False)

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
    status = db.Column(db.Integer, db.ForeignKey("table_status.id"), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=True)
    status = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return "Table object: name=%s" % self.name


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
    # income = db.Column(db.String(64), nullable=False)
    # dishes_id = db.Column(db.Integer, db.ForeignKey("menu.id"))

    def __repr__(self):
        return "Order object: name=%s" % self.name


class Detail(db.Model):
    __tablename__ = "detail"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)  # 主键自增，唯一，不可为空
    dish_id = db.Column(db.Integer, db.ForeignKey("menu.id"), nullable=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=True)
    # dishes_id = db.Column(db.Integer, db.ForeignKey("menu.id"))

    def __repr__(self):
        return "Detail object: name=%s" % self.name
