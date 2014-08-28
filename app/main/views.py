from flask import render_template, redirect, url_for
from flask.ext.login import login_required, current_user
from . import main
from .forms import RequestPluginForm
from .. import db
from ..email import send_email
from ..models import User, Order, Plugin, PluginConfig, PluginPermission, \
                     PluginCommand, PluginEvent
from datetime import datetime

@main.before_request
def before_request():
    if current_user.is_authenticated():
        current_user.last_seen = datetime.utcnow()


@main.route('/')
def index():
    return render_template("index.html")

@login_required
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

        plugin = Plugin(name = form.plugin_name.data,
                        description = form.plugin_desc.data,
                        commands = commands,
                        permissions = permissions,
                        configs = configs,
                        events = events)
        db.session.add(plugin)

        order = Order(plugin_id = plugin.id,
                      user_id = current_user.id)
        db.session.add(order)
        db.session.commit()

        order = Order(plugin_id = plugin.id,
                      user_id = current_user.id)
        db.session.add(order)
        db.session.commit()

        send_email(current_user.email, 'Success: Your plugin has been listed!',
                   'mail/plugin_added', user=current_user, plugin=plugin)
        return redirect(url_for('dashboard.dash'))
    return render_template("order.html", form=form)


