from flask import render_template, redirect, request, url_for, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
import balanced
from . import auth
from .. import db
from ..models import User, Plugin, Order
from ..email import send_email
from .forms import PaymentForm, LoginForm, RegistrationForm, ChangePasswordForm, \
                   PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm

class PaymentManager(object):
    def __init__(self, request):
        super(PaymentManager, self).__init__()
        self.request = request

    def pay(self, order, card_uri):
        db.session.flush()
        user = current_user

        if not user.account_uri:
            self.create_balanced_account(user, card_uri)
        else:
            if card_uri:
                user.add_card(card_uri)
        db.session.flush()
        return order.debit(user, card_uri)

    def create_balanced_account(self, user, card_uri):
        try:
            user.create_balanced_account(card_uri=card_uri)
        except balanced.exc.HTTPError as ex:
            if (ex.status_code == 409 and
            'email_address' in ex.description):
                user.associate_balanced_account()
            else:
                raise ex

@auth.route('/pay/<int:order_id>', methods=['GET', 'POST'])
@login_required
def pay(order_id):
    form = PaymentForm()
    order = Order.query.get_or_404(order_id)
    if not current_user.id == order.user_id:
        abort(504)
    elif order.paid == True:
        return redirect(url_for('auth.receipt', order_id=order_id))

    if form.validate_on_submit():
        manager = PaymentManager(request)
        card_uri = request.form.get('card_uri', None)
        try:
            manager.pay(order, card_uri)
        except balanced.exc.HTTPError as ex:
            msg = 'Error debiting account, your card has not been charged "{}"'
            flash(msg.format(ex.message), 'error')
            db.session.rollback()
        except Exception as ex:
            raise
        else:
            db.session.commit()
            return redirect(url_for('auth.receipt', order_id=order_id))
    return render_template('auth/pay.html', form=form, order=order)

@auth.route('/receipt/<int:order_id>')
@login_required
def receipt(order_id):
    order = Order.query.get_or_404(order_id)
    plugin = Plugin.query.get_or_404(order.plugin_id)
    if not current_user.id == order.user_id:
        abort(504)
    elif not order.paid:
        abort(404)

    return render_template('auth/receipt.html', plugin=plugin, order=order)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)#, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('dashboard.dash'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email    = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm your account',
                   'auth/mail/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/mail/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/mail/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
            flash('An email with instructions to reset your password has been '
                  'sent to you.')
            return redirect(url_for('auth.login'))
        else:
            flash('Email not found.')
    return render_template('auth/reset_password_request.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous():
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/mail/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)

@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))
