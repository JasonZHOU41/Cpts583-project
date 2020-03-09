# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, IntegerField
from wtforms import TextField, FormField, SelectField, FieldList, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(1, 20)], render_kw={"placeholder": "User Name/ Work Number"})
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(6, 20)], render_kw={"placeholder": "Password"})
    # remember = BooleanField('Remember me', default=False)
    submit = SubmitField('Log in')
