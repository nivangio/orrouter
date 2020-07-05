from flask import Blueprint, request
import traceback
from flask_json import JsonError, as_json
from Item import Item

item_views = Blueprint("item_views", __name__)

@item_views.route('/items', methods=['GET'])
@as_json
def get_items():

    all_items = Item.get_all()
    elems = list(map(lambda x: x.to_dict(), all_items))

    return {"rows": elems}


@item_views.route('/submit_item', methods=['POST'])
@as_json
def submit_items():
    config = request.get_json(force=True)

    if config["id"] is None:
        config.pop("id")
        Item.create(**config)
    else:
        to_change = Item.get_by_id(config.pop("id"))
        to_change.update(**config)

    return {}
