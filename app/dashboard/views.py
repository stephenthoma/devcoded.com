from flask import render_template, redirect, url_for, abort, flash, request, \
                  current_app, make_response
from flask.ext.login import login_required, current_user
from . import dashboard
from .. import db
from ..models import User

@dashboard.route('/')
@login_required
def dash():
    return render_template("dashboard/dashboard.html")

@dashboard.route('/orders')
@login_required
def orders():
    return render_template("dashboard/orders.html")

@dashboard.route('/history')
@login_required
def history():
    return render_template("dashboard/history.html")
