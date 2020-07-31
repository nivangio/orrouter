from flask import Blueprint, request
import traceback
from flask_json import JsonError, as_json
from starter import db_session
from Client import Client

client_views = Blueprint("client_views", __name__)

@client_views.route('/clients', methods=['GET'])
@as_json
def get_clients():

    all_clients = Client.get_all()
    elems = list(map(lambda x: {**x.to_dict(), **{"address_display": x.display_address()}}, all_clients))

    return {"rows": elems}


@client_views.route('/submit_client', methods=['POST'])
@as_json
def submit_client():
    config = request.get_json(force=True)
    try:
        if config["id"] is None:
            config.pop("id")
            Client.create(**config)
        else:
            to_change = Client.get_by_id(config.pop("id"))
            to_change.update(**config)

    except Exception as e:
        traceback.print_exc()
        raise JsonError(description=e.args[0])

    return {}

@client_views.route('/clients_options', methods=['GET'])
@as_json
def get_client_options():

    all_clients = Client.get_all()
    elems = list(map(lambda x: x.to_options("company_name"), all_clients))

    return {"options": elems}
