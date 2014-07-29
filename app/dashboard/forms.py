from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms_html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, Regexp


class SettingsForm(Form):
    email = EmailField('Email', validators=[DataRequired(), Length(1, 64),
                                            Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8,64, message='Password must be more than 8 characters long.')])
    update = SubmitField('Update')
    delete = SubmitField('Delete account')
