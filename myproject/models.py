# -*- coding: utf-8 -*-

from myproject import db
from flask import current_app


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    #  users = db.relationship("User", backref="role")

    def __repr__(self):
        return "Role object: name=%s" % self.name


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return "User object: name=%s" % self.name

    @staticmethod
    def init_admin():
        db.drop_all()
        db.create_all()
        u1 = User()
        u1.name = "Admin"
        u1.password = "Admin_Password"
        u1.email = "350535629@qq.com"
        db.session.add(u1)
        db.session.commit()
