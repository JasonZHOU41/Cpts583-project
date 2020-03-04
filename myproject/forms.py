# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, IntegerField
from wtforms import TextField, FormField, SelectField, FieldList, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('username',
                           validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(6, 20)])
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField()
