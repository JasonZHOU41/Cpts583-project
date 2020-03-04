# -*- coding: utf-8 -*-


import os
from flask import Flask
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object('config')

bootstrap = Bootstrap(app)


from myproject import views
