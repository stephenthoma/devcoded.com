from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import balanced
from flask import current_app, request, url_for
from flask.ext.login import UserMixin, AnonymousUserMixin
from . import db, login_manager

class Role:
    ADMIN = 0x03
    DEV   = 0x02
    USER  = 0x01

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    account_uri = db.Column(db.Unicode, unique=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True)
    role = db.Column(db.Integer, default=Role.USER)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                    username=forgery_py.lorem_ipsum.word(),
                    password=forgery_py.lorem_ipsum.word(),
                    confirmed=True)
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['DEVCODED_ADMIN']:
                self.role = Role.ADMIN
            if self.role is None:
                self.role = Role.USER

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query_filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    @property
    def balanced_account(self):
        if self.account_uri:
            return balanced.Customer.fetch(self.account_uri)

    def create_balanced_account(self, card_uri=None,
                                merchant_data=None):
        if self.account_uri:
            raise Exception('User already has a balanced account')
        if card_uri:
            account = self._create_balanced_buyer(card_uri)
        else:
            account = self._create_balanced_merchant(merchant_data)
        self.associate_balanced_account(account.href)
        return account

    def _create_balanced_buyer(self, card_uri):
        try:
            account = balanced.Customer(email=self.email,
                                        name=self.username).save()
            card = balanced.Card.fetch(card_uri)
            card.associate_to_customer(account.href)
        except balanced.exc.HTTPError as ex:
            # if 500 then this attribute is not set...
            if getattr(ex, 'category_code', None) == 'duplicate-email-address':
                # account already exists, let's upsert
                account = balanced.Customer.query.filter(
                    email_address=self.email).one()
                card = balanced.Card.fetch(card_uri)
                card.associate_to_customer(account.href)
            else:
                raise
        return account

    def _create_balanced_merchant(self, merchant_data):
        marketplace = balanced.Marketplace.my_marketplace
        try:
            account = marketplace.create_merchant(self.email,
                name=self.username, merchant=merchant_data)
        except balanced.exc.HTTPError as ex:
            if getattr(ex, 'category_code', None) == 'duplicate-email-address':
                # account already exists, let's upsert
                account = marketplace.accounts.filter(
                    email_address=self.email).one()
                if 'merchant' in account.roles:
                    merchant_data.pop('dob')
                    merchant_data.pop('state')
                account.add_merchant(merchant_data)
            else:
                raise
        return account

    def lookup_balanced_account(self):
        if self.account_uri:
            return
        try:
            account = balanced.Account.query.filter(
                email_address=self.email).one()
        except balanced.exc.NoResultFound:
            pass
        else:
            self.account_uri = account.href

    def associate_balanced_account(self, account_uri=None):
        """
        Assign a Balanced account_uri to a user. This will check that the
        email addresses within balanced and our local system match first. It
        will also fail if the local user already has an account assigned.
        """
        if account_uri:
            balanced_email_address = balanced.Customer.fetch(
                account_uri).email
        else:
            balanced_email_address = balanced.Customer.filter(
                email_address=self.email).one()
        if balanced_email_address != self.email:
            # someone is trying to claim an account that doesn't belong to them
            raise Exception('Email address mismatch.')
        if self.account_uri and self.account_uri != account_uri:
            # it shouldn't be possible to claim another account
            raise Exception('Account mismatch')
        self.account_uri = account_uri

    def add_card(self, card_uri):
        """
        Adds a card to an account within Balanced.
        """
        try:
            account = balanced.Customer.query.filter(
                email_address=self.email).one()
        except balanced.exc.NoResultFound:
            account = balanced.Customer(
                email=self.email,
                name=self.username).save()
        card = balanced.Card.fetch(card_uri)
        card.associate_to_customer(account.href)
        return account

    def add_merchant(self, merchant_data):
        if 'merchant' in self.balanced_account.roles:
            merchant_data.pop('dob')
            merchant_data.pop('state')
        self.balanced_account.add_merchant(merchant_data)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Plugin(db.Model):
    __tablename__ = 'plugins'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(64))
    description = db.Column(db.Text)
    commands = db.relationship('PluginCommand')
    permissions = db.relationship('PluginPermission')
    configs = db.relationship('PluginConfig')
    events = db.relationship('PluginEvent')

class PluginConfig(db.Model):
    __tablename__ = 'plugin_configs'
    id = db.Column(db.Integer, primary_key=True)
    plugin_id = db.Column(db.Integer, db.ForeignKey('plugins.id'))
    name = db.Column(db.String(64))
    value = db.Column(db.String(64))
    description = db.Column(db.Text())

class PluginPermission(db.Model):
    __tablename__ = 'plugin_perms'
    id = db.Column(db.Integer, primary_key=True)
    plugin_id = db.Column(db.Integer, db.ForeignKey('plugins.id'))
    node = db.Column(db.String(64))
    description = db.Column(db.Text())

class PluginCommand(db.Model):
    __tablename__ = 'plugin_commands'
    id = db.Column(db.Integer, primary_key=True)
    plugin_id = db.Column(db.Integer, db.ForeignKey('plugins.id'))
    command = db.Column(db.String(64))
    node = db.Column(db.String(64))
    description = db.Column(db.Text())

class PluginEvent(db.Model):
    __tablename__ = 'plugin_events'
    id = db.Column(db.Integer, primary_key=True)
    plugin_id = db.Column(db.Integer, db.ForeignKey('plugins.id'))
    action = db.Column(db.Text())
    result = db.Column(db.Text())

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    plugin_id = db.Column(db.Integer, db.ForeignKey('plugins.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    paid = db.Column(db.Boolean, default=False)
    price = db.Column(db.Integer)
    href = db.Column(db.Unicode)

    def debit(self, user, card_uri=None):
        account = User.balanced_account
        if not card_uri:
            if not account.cards.count():
                raise Exception('No card on file')
            if not user.has_password:
                raise Exception('Anonymous users must specify a card')

        # this will throw balanced.exc.HTTPError if it fails
        try:
            card = balanced.Card.fetch(card_uri)
            debit = card.debit(
                    appears_on_statement_as = 'DevCoded LLC. order #{0}'.format(self.id),
                    amount = self.price / 100,
                    description='Hold for order #{0} of plugin {1}'.format(self.id, self.plugin_id))
        except balanced.exc.HTTPError as ex:
            raise ex
        else:
            self.href = debit.href
            self.paid = True

    def readable_price(self):
        if not self.price:
            return '$0.00'
        else:
            return '$' + '{:.2f}'.format(float(self.price) / 1000)

