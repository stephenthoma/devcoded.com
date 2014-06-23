from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp
from wtforms import ValidationError
from ..models import User

class RequestPluginForm(Form):
    # [TODO]: Design this form
    name = StringField('Plugin name?', validators=[Required()])

