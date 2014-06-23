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

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html")

@main.route('/order')
def order():
    return render_template("order.html")
