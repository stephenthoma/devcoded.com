from flask import render_template, redirect, url_for, abort, flash, request, \
                  current_app, make_response
from flask.ext.login import login_required, current_user
from . import dashboard
from .. import db
from ..models import User, Role
from .forms import SettingsForm

@dashboard.route('/')
@login_required
def dash():
    user_role = current_user.role
    if user_role  == Role.USER:
        return render("dashboard_user")
    elif user_role == Role.DEV:
        return render("dashboard_developer")
    elif user_role == Role.ADMIN:
        return render("dashboard_admin")

@dashboard.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    #TEMPORALY
    form = SettingsForm()
    if form.validate_on_submit():
        flash('submitted')

    return render_template("dashboard/dashboard_settings.html", form=form)

def render(url):
    if not url.endswith(".html"):
        url += ".html"
    return render_template("dashboard/" + url)
