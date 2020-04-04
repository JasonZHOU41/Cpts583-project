# -*- coding: utf-8 -*-


import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import flask_monitoringdashboard as dashboard


app = Flask(__name__)
dashboard.bind(app)
app.config.from_object('config')

bootstrap = Bootstrap(app)
db = SQLAlchemy()
db.init_app(app)
# db.create_all()

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'


from myproject import views, models

