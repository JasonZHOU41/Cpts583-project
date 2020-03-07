# -*- coding: utf-8 -*-


import os


CSRF_ENABLED = True
SECRET_KEY = 'Spark315'
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(basedir,
                                                'myproject-dev.sqlite3')

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True
