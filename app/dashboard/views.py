from flask import render_template, redirect, url_for, abort, flash, request, \
                  current_app, make_response
from flask.ext.login import login_required, current_user
from . import dashboard
from .. import db
from ..models import User, Role
from .forms import SettingsForm

@dashboard.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@dashboard.route('/<path:path>')
@login_required
def dash(path):
    form = SettingsForm()
    if form.validate_on_submit():
        flash('submitted')

    return render_template("dashboard/dashboard_" + current_user.readable_role() + ".html", form=form)

@dashboard.route('/settings', )
@login_required
def settings():
    #TEMPORALY
    form = SettingsForm()
    if form.validate_on_submit():
        flash('submitted')

    return render_template("dashboard/user_settings.html", form=form)

def render(url):
    if not url.endswith(".html"):
        url += ".html"
    return render_template("dashboard/" + url)
