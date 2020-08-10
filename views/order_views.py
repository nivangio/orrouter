from flask import Blueprint, request
import traceback
from flask_json import JsonError, as_json
from starter import db_session
from orders import Order
from sqlalchemy import func
from datetime import date

order_views = Blueprint("orders_views", __name__)


@order_views.route('/orders', methods=['GET'])
@as_json
def get_orders():

    client_id = request.args.get("client_id",None)

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
        if config["id"] is None:
            config.pop("id")
            Order.create(**config)
        else:
            to_change = Order.get_by_id(config.pop("id"))
            to_change.update(**config)


    except Exception as e:
        Order.rollback()
        traceback.print_exc()
        raise JsonError(description=e.args[0])


    return {}

@order_views.route('/order_dates_options', methods=['GET'])
@as_json
def get_unique_orders_dates():

    res = db_session.query(func.Date(Order.arrive_before)).filter(
                ##Created and/or scheduled for delivery not
                Order.status_id.in_([1,2]),
                func.Date(Order.arrive_before) >= date.today()
            ).distinct().all()

    unique_order_dates = list(map(lambda x: x[0], res))

    #ret = list(map(lambda x: x.to_dict(), unique_order_dates))

    return {"options": unique_order_dates}
