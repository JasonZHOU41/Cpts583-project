# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect
from myproject import app
from .forms import LoginForm


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title="It's the index")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title="Sign In", form=form)



