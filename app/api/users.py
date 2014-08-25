from flask import jsonify, request, current_app, url_for
from .. import db
from . import api
from .helpers import respond
from .decorators import permission_required
from ..models import User, Plugin, Order, Role

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(respond(200, user.to_json()))

@api.route('/users/<int:id>/role', methods=['GET','POST'])
@permission_required(Role.ADMIN)
def user_role(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        role = request.get_json()['role']
        if role in [1,2]:
            user.role = role
            db.session.commit
        else:
            return jsonify(response(500))
    return jsonify(response(200, {user.role}))

@api.route('/users/<int:id>/plugins/')
def get_user_plugins(id):
    user = User.query.get_or_404(id)
    plugins = Plugin.query.filter_by(user_id=user.id).all()
    x = list()
    for p in plugins:
        x.append(p.id)
    return jsonify(respond(200, {'plugin_ids': x}))

@api.route('/users/<int:id>/orders/')
def get_user_orders(id):
    user = User.query.get_or_404(id)
    orders = Order.query.filter_by(user_id=user.id).all()
    x = list()
    for o in orders:
        x.append(o.id)
    return jsonify(respond(200, {'order_ids': x}))

@api.route('/users/search/<username>')
def get_user_id(username):
    try: id = User.query.filter_by(username=username).first().id
    except: return jsonify(respond(404))
    return jsonify(respond(200, {'username': username, 'id': id}))
