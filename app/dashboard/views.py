from flask import render_template, redirect, url_for, abort, flash, request, \
                  current_app, make_response
from flask.ext.login import login_required, current_user
from . import dashboard
from .. import db
from ..models import User, Role

@dashboard.route('/')
@login_required
def dash():
    user_role = current_user.role
    if user_role  == Role.USER:
        return render_template("dashboard/dashboard_user.html")
    elif user_role == Role.DEV:
        return render_template("dashboard/dashboard_developer.html")
    elif user_role == Role.ADMIN:
        return render_template("dashboard/dashboard_admin.html")
