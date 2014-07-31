from flask.ext.wtf import Form
from wtforms import PasswordField, BooleanField, SubmitField
from wtforms_html5 import EmailField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Optional


class SettingsForm(Form):
  email = EmailField('Change email', validators=[Optional(),Email()])
  password = PasswordField('New password', validators=[Optional(),
    Length(8, 64, message='Password must be more than 8 characters long.'),
    EqualTo('password2', message='Passwords must match ')])
  password2 = PasswordField('Password again', validators=[])

  receiveMail = BooleanField('Receive update mails')
  option1 = BooleanField('Option 1')
  option2 = BooleanField('Option 2')
  option3 = BooleanField('Option 3')

  passwordConfirm = PasswordField('Password confirmation', validators=[InputRequired(message="You must confirm with your current password"), Length(8, 64)])
  submit = SubmitField('Update')

