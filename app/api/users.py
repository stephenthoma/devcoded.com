from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User, Plugin

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())

@api.route('/users/<int:id>/plugins/')
def get_user_plugins(id):
    user = User.query.get_or_404(id)
    plugins = Plugin.query.filter_by(user_id=user.id).all()
    x = list()
    for p in plugins:
        x.append(p.id)
    return jsonify({'plugin_ids': x})

@api.route('/users/search/<username>')
def get_user_id(username):
    id = User.query.filter_by(username=username).first().id
    return jsonify({'id': id})
