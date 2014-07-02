from flask import render_template, redirect, url_for, abort, flash, request, \
                  current_app, make_response
from flask.ext.login import login_required, current_user
from . import main
from .forms import RequestPluginForm
from .. import db
from ..models import User

@main.route('/')
def index():
    return render_template("index.html")

@main.route('/order')
def order():
    return render_template("order.html")

# Dashboard parts

@main.route('/dashboard')
@main.route('/dashboard/')
@main.route('/dashboard/??ANYTHINGELSE??')
@login_required
def dashboard():
    return render_template("dashboard/dashboard.html")

@main.route('/dashboard/orders')
@login_required
def orders():
    return render_template("dashboard/orders.html")

@main.route('/dashboard/history')
@login_required
def history():
    return render_template("dashboard/history.html")
