from flask.ext.wtf import Form
from wtforms import Form as insecureForm
from wtforms import StringField, TextAreaField, FormField, FieldList
from wtforms.validators import DataRequired, Length, Optional

# insecureForm doesn't have CSRF! Only use in FormFields
# that will be subforms of normal, secure, forms.

class CommandForm(insecureForm):
    command_name = StringField('Command name', validators=[DataRequired(), Length(1, 32)])
    command_perm = StringField('Command permission', validators=[DataRequired(), Length(1, 32)])
    command_desc = StringField('Command description', validators=[DataRequired(), Length(1, 128)])

class PermissionsForm(insecureForm):
    permission_name = StringField('Permission name', validators=[Optional(), Length(1, 32)])
    permission_desc = StringField('Permission description', validators=[Optional()])

class ConfigurationForm(insecureForm):
    config_name = StringField('Configuration option', validators=[DataRequired(), Length(1, 32)])
    config_val = StringField('Default value', validators=[DataRequired(), Length(1,32)])
    config_desc = StringField('Description', validators=[DataRequired(), Length(1, 128)])

class EventForm(insecureForm):
    action = StringField('Event action', validators=[DataRequired(), Length(1,64)])
    result = StringField('Event result', validators=[DataRequired(), Length(1,64)])

class RequestPluginForm(Form):
    plugin_name = StringField('Plugin name', validators=[DataRequired(), Length(1, 64)])
    plugin_desc = TextAreaField('Plugin description', validators=[DataRequired(), Length(1, 256)])
    commands    = FieldList(FormField(CommandForm))
    permissions = FieldList(FormField(PermissionsForm))
    configs     = FieldList(FormField(ConfigurationForm))
    events      = FieldList(FormField(EventForm))

