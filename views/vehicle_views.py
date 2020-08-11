from flask import Blueprint, request
import traceback
from flask_json import JsonError, as_json
from auth import token_required

from Vehicle import Vehicle

vehicle_views = Blueprint("vehicle_views", __name__)

@vehicle_views.route('/vehicles', methods=['GET'])
@token_required
@as_json
def get_vehicle(requesting_user):

    all_vehicles = Vehicle.get_all(requesting_user.id)
    elems = list(map(lambda x: x.to_dict(), all_vehicles))

    return {"rows": elems}


@vehicle_views.route('/submit_vehicle', methods=['POST'])
@token_required
@as_json
def submit_vehicle(requesting_user):
    try:
        config = request.get_json(force=True)
        if config["id"] is None:
            config.pop("id")
            config["user_id"] = requesting_user.id
            Vehicle.create(**config)
        else:
            to_change = Vehicle.get_by_id(config.pop("id"))
            to_change.update(**config)

    except Exception as e:
        traceback.print_exc()
        raise JsonError(description=e.args[0])

    return {}

@vehicle_views.route('/vehicles_options', methods=['GET'])
@token_required
@as_json
def get_vehicle_options(requesting_user):

    all_items = Vehicle.get_all(requesting_user.id)
    elems = list(map(lambda x: x.to_options("vehicle_name"), all_items))

    return {"options": elems}