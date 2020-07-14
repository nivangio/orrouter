from flask import Blueprint, request
import traceback
from flask_json import JsonError, as_json
from starter import db_session
from orders import Order

order_views = Blueprint("orders_views", __name__)


@order_views.route('/orders', methods=['GET'])
@as_json
def get_orders():

    client_id = request.args.get("client",None)

    if client_id is None:
        orders = Order.get_all()
    else:
        orders = Order.get(client_id=client_id, multiple=True)

    ret = list(map(lambda x: x.to_dict(), orders))

    return {"rows":ret}