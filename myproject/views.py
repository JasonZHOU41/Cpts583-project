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


@app.route('/Employee', methods=['GET', 'POST'])
def employee():
    return render_template('employee.html', title="Employee")


@app.route('/employer', methods=['GET', 'POST'])
def employer():
    return render_template('employer.html', title="Employer")


@app.route('/TableState', methods=['GET', 'POST'])
def table():
    return render_template('table.html', title="Table")


@app.route('/Menu', methods=['GET', 'POST'])
def menu():
    return render_template('menu.html', title="Menu")


@app.route('/OrderState', methods=['GET', 'POST'])
def order():
    return render_template('order.html', title="Order")

