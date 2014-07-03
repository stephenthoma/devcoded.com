from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField, \
                    SubmitField, ValidationError, FormField, FieldList
from wtforms.validators import DataRequired, Length, Email, Regexp

class CommandForm(Form):
    command_name = StringField('Command name', validators=[DataRequired(), Length(1, 32)])
    command_perm = StringField('Command permission', validators=[DataRequired(), Length(1, 32)])
    command_desc = StringField('Command description', validators=[DataRequired(), Length(1, 128)])

class PermissionsForm(Form):
    permission_name = StringField('Permission name', validators=[DataRequired(), Length(1, 32)])
    permission_desc = StringField('Permission description', validators=[DataRequired(), Length(1, 128)])

class ConfigurationForm(Form):
    config_name = StringField('Configuration option', validators=[DataRequired(), Length(1, 32)])
    config_val = StringField('Default value', validators=[DataRequired(), Length(1,32)])
    config_desc = StringField('Description', validators=[DataRequired(), Length(1, 128)])

class EventForm(Form):
    action = StringField('Event action', validators=[DataRequired(), Length(1,64)])
    result = StringField('Event result', validators=[DataRequired(), Length(1,64)])

class RequestPluginForm(Form):
    plugin_name = StringField('Plugin name', validators=[DataRequired(), Length(1, 64)])
    plugin_desc = TextAreaField('Plugin description', validators=[DataRequired(), Length(1, 256)])
    commands    = FormField(CommandForm)
    permissions = FormField(PermissionsForm)
    configs     = FormField(ConfigurationForm)
    events      = FormField(EventForm)

