from flask import render_template, redirect, url_for, abort, flash, request, \
                  current_app, make_response
from flask.ext.login import login_required, current_user
from . import dashboard
from .. import db
from ..models import User, Role
from .forms import SettingsForm

@dashboard.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@dashboard.route('/<path:path>', methods=['GET', 'POST'])
@login_required
def dash(path):
    form = SettingsForm()
    if form.validate_on_submit():
      if not current_user.verify_password(form.passwordConfirm):
        #entered wrong password
        flash("Wrong confirmation password")

      flash('submitted')
    flash("test")
    return render_template("dashboard/dashboard_" + current_user.readable_role() + ".html", form=form)
