# -*- coding: utf-8 -*-


import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('config')

bootstrap = Bootstrap(app)
db = SQLAlchemy()
db.init_app(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


from myproject import views, models

