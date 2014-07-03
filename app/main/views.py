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

@main.route('/order', methods=['GET', 'POST'])
def order():
    form = RequestPluginForm()
    if request.method == 'POST':
        raise

    if form.validate_on_submit():
        #[TODO]: Add plugin to database
        #[TODO]: Notify admin plugin was submitted
        return redirect(url_for('dashboard.dash'))
    return render_template("order.html", form=form)


