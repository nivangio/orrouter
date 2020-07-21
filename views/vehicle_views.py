from flask import Blueprint, request
import traceback
from flask_json import JsonError, as_json

from Vehicle import Vehicle

vehicle_views = Blueprint("vehicle_views", __name__)

@vehicle_views.route('/vehicles', methods=['GET'])
@as_json
def get_vehicle():

    all_vehicles = Vehicle.get_all()
    elems = list(map(lambda x: x.to_dict(), all_vehicles))

    return {"rows": elems}


@vehicle_views.route('/submit_vehicle', methods=['POST'])
@as_json
def submit_vehicle():
    try:
        config = request.get_json(force=True)
        if config["id"] is None:
            config.pop("id")
            Vehicle.create(**config)
        else:
            to_change = Vehicle.get_by_id(config.pop("id"))
            to_change.update(**config)

    except Exception as e:
        traceback.print_exc()
        raise JsonError(description=e.args[0])

    return {}

