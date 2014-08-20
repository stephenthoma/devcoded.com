from flask import jsonify, request, current_app, url_for
from . import api
from .helpers import respond
from ..models import User, Plugin, Order, Role

@api.route('/orders/')
def get_all_orders():
    json_orders = list()
    orders = Order.query.all()
    for order in orders:
        json_orders.append(order.to_json())
    return jsonify(respond(200, {'orders': json_orders}))

@api.route('/orders/<int:id>')
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify(respond(200, order.to_json()))

@api.route('/orders/<int:id>/delete/', methods=['DELETE'])
@permission_required(Role.ADMIN)
def delete_order(id):
    order = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify(respond(200))
