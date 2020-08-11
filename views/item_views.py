from flask import Blueprint, request
import traceback
from flask_json import JsonError, as_json
from Item import Item
from auth import token_required

item_views = Blueprint("item_views", __name__)

@item_views.route('/items', methods=['GET'])
@token_required
@as_json
def get_items(requesting_user):

    try:
        all_items = Item.get_all(requesting_user.id)
        elems = list(map(lambda x: x.to_dict(), all_items))

    except Exception as e:
        traceback.print_exc()
        raise JsonError(description=e.args[0])

    return {"rows": elems}


@item_views.route('/submit_item', methods=['POST'])
@token_required
@as_json
def submit_items(requesting_user):
    config = request.get_json(force=True)
    try:
        if config["id"] is None:
            config.pop("id")
            config["user_id"] = requesting_user.id
            Item.create(**config)
        else:
            to_change = Item.get_by_id(config.pop("id"))
            to_change.update(**config)

    except Exception as e:
        traceback.print_exc()
        raise JsonError(description=e.args[0])

    return {}

@item_views.route('/items_options', methods=['GET'])
@token_required
@as_json
def get_item_options(requesting_user):
    try:
        all_items = Item.get_all(requesting_user.id)
        elems = list(map(lambda x: x.to_options("item_name"), all_items))

    except Exception as e:
        traceback.print_exc()
        raise JsonError(description=e.args[0])

    return {"options": elems}
