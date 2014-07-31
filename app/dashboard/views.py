from flask import render_template, flash
from flask.ext.login import login_required, current_user
from wtforms import ValidationError

from . import dashboard
from ..models import User
from .forms import SettingsForm


@dashboard.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@dashboard.route('/<path:path>', methods=['GET', 'POST'])
@login_required
def dash(path):
  form = SettingsForm()

  if form.validate_on_submit():
    if current_user.verify_password(form.passwordConfirm.data):
      if (form.password.data and form.password.data == form.password2.data and not current_user.verify_password(form.password.data)):
        # change password, not empty and password not same as old
        flash("new password = " + form.password.data)
      if form.email.data and not form.email.data == current_user.email:
        # change email, not empty, not same,
        if User.query.filter_by(email=form.email.data).first():
          raise ValidationError('Email already registered.')
          # email in use
          flash("email in use")
        else:
          flash("email changed to " + form.email.data)
          # we good
          # set options
      flash("Settings updated")
    else:
      # entered wrong password
      flash("Wrong confirmation password")

  return render_template("dashboard/dashboard_" + current_user.readable_role() + ".html", form=form)
