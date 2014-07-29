from flask.ext.wtf import Form
from wtforms import PasswordField, BooleanField, SubmitField, ValidationError
from wtforms_html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from app.models import User

class SettingsForm(Form):
    email = EmailField('Change email', validators=[
        DataRequired(),
        Length(1, 64),
        Email()])
    password = PasswordField('New password', validators=[
        DataRequired(),
        Length(8,64, message='Password must be more than 8 characters long.'),
        EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    receiveMail = BooleanField('Receive update mails')
    option1 = BooleanField('Option 1')
    option2 = BooleanField('Option 2')
    option3 = BooleanField('Option 3')

    password2 = PasswordField('Password confirmation', validators=[DataRequired()])

    update = SubmitField('Update')
    delete = SubmitField('Delete account')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

