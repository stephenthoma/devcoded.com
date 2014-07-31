from flask import render_template, flash
from flask.ext.login import login_required, current_user

from ..email import send_email
from .. import db

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
        current_user.password = form.password.data
        db.session.add(current_user)
        flash('Your password has been updated.')
      if form.email.data and not form.email.data == current_user.email:
        # change email, not empty, not same,
        if User.query.filter_by(email=form.email.data).first():
          # email in use
          flash('Email already registered.')
        else:
          new_email = form.email.data
          token = current_user.generate_email_change_token(new_email)
          send_email(new_email, 'Confirm your email address',
                     'auth/mail/change_email',
                     user=current_user, token=token)
          flash('An email with instructions to confirm your new email '
                'address has been sent to you.')
    else:
      # entered wrong password
      flash("Wrong confirmation password")

  return render_template("dashboard/dashboard_" + current_user.readable_role() + ".html", form=form)
