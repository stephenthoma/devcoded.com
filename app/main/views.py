from flask import render_template, redirect, url_for, abort, flash, request, \
                  current_app, make_response
from flask.ext.login import login_required, current_user
from . import main
from .forms import RequestPluginForm
from .. import db
from ..email import send_email
from ..models import User, Plugin, PluginConfig, PluginPermission, \
                     PluginCommand, PluginEvent

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/order', methods=['GET', 'POST'])
def order():
    form = RequestPluginForm()

    if form.validate_on_submit():
        commands = []; permissions = []; configs = []; events = []
        for field in form.commands.data:
            commands.append(PluginCommand(command=field['command_name'],
                                          node=field['command_perm'],
                                          description=field['command_desc']))
        for field in form.permissions.data:
            permissions.append(PluginPermission(node=field['permission_name'],
                                                description=field['permission_desc']))

        for field in form.configs.data:
            configs.append(PluginConfig(name=field['config_name'],
                                        value=field['config_val'],
                                        description=field['config_desc']))
        for field in form.events.data:
            events.append(PluginEvent(action=field['action'],
                                      result=field['result']))

        plugin = Plugin(user_id = current_user.id,
                        name = form.plugin_name.data,
                        description = form.plugin_desc.data,
                        commands = commands,
                        permissions = permissions,
                        configs = configs,
                        events = events)
        db.session.add(plugin)
        db.session.commit()

        send_email(current_user.email, 'Success: Your plugin has been listed!',
                   'mail/plugin_added', user=current_user, plugin=plugin)
        return redirect(url_for('dashboard.dash'))
    return render_template("order.html", form=form)


