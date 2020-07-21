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

@order_views.route('/submit_order', methods=['POST'])
@as_json
def submit_orders():

    config = request.get_json(force=True)

    ##Parse request
    config["items"] = list(map(lambda x: {"id":x["item"]["id"], "quantity": x["quantity"]}, config.pop("order")))
    config["client_id"] = config.pop("client")["id"]

    try:
        Order.create(**config)
    except Exception as e:
        Order.rollback()
        traceback.print_exc()
        raise JsonError(description=e.args[0])


    return {}
