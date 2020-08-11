###TODO: This should go to some kind of config or be replaced by getenv if Dockerized
#ROUTING_API_URL = "http://10.0.0.155:5000/get_optimal_route"
ROUTING_API_URL = "http://127.0.0.1:5001/get_optimal_route"

from orders import Order
from starter import db_session
from Client import Client
from User import User
from requests import post
from sqlalchemy import Date, cast
from json import dumps, loads

def create_route(user_id, start, end, vehicles):

    post_element = {}
    post_element["vehicles"] = list(map(lambda x: {"vehicle_capacity": int(x.capacity)}, vehicles))
    post_element["starting_time"] = int(start.timestamp())

    depot = User.get_by_id(user_id).address

    post_element["starting_location"] = {"lat":depot["geometry"]["coordinates"][1], "long":depot["geometry"]["coordinates"][0]}

    orders_to_deliver = db_session.query(Order)\
                                  .join(Client)\
                                  .filter(Client.user_id == user_id,
                                          cast(Order.arrive_after, Date) == start.date()).all()

    post_element["directions"] = list(map(lambda x: {"long": x.client.address["geometry"]["coordinates"][0],
                                                     "lat": x.client.address["geometry"]["coordinates"][1],
                                                     "arrive_before": int(x.arrive_before.timestamp()),
                                                     "arrive_after": int(x.arrive_after.timestamp()),
                                                     "demands":x.total_volume()},
                                          orders_to_deliver))


    ret = post(ROUTING_API_URL, data = dumps(post_element))

    if ret.status_code != 200:
        raise ValueError("Optimizer error: {}".format(loads(ret.text)["description"]))

    return ret