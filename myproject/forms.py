# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, IntegerField
from wtforms import TextField, FormField, SelectField, FieldList, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(1, 20)],
                           render_kw={"placeholder": "User Name/ Work Number"})
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(6, 20)],
                             render_kw={"placeholder": "Password"})
    # remember = BooleanField('Remember me', default=False)
    submit = SubmitField('Log in')


class Add_Form(FlaskForm):
    '''

    Creat the new account for the employee

    '''
    username = StringField('Username',
                           validators=[DataRequired(), Length(1, 20)],
                           render_kw={"placeholder": "User Name/ Work Number"})

    password = PasswordField('Password',
                             validators=[DataRequired(), Length(6, 20)],
                             render_kw={"placeholder": "Password"})

    password_again = PasswordField('Confirm Password',
                            validators=[DataRequired(), Length(6, 20)],
                            render_kw={"placeholder": "Confirm Password"})

    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "Email Address"})

    name = StringField('Full Name',
                       validators=[DataRequired()],
                       render_kw={"placeholder": "Name"})

    role = SelectField('Role',
                       choices=[('1', 'Waiter'),
                                ('2', 'Host'),
                                ('3', 'Kitchen'),
                                ('4', 'Busboy'),
                                ('5', 'Manager')])

    add = SubmitField('Add')


# class Employer_Search(FlaskForm):
#     '''
#     员工查找
#     '''
#
#
# class Order_Search(FlaskForm):
#     '''
#     订单查询
#     '''
