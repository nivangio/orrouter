from flask import Blueprint, request
import traceback
from flask_json import JsonError, as_json
from auth import token_required

user_views = Blueprint("user_views", __name__)

@user_views.route('/change_address', methods=['POST'])
@token_required
@as_json
def change_address(requesting_user):
    config = request.get_json(force=True)
    try:
        requesting_user.update(address = config["address"])

    except Exception as e:
        traceback.print_exc()
        raise JsonError(description=e.args[0])

    return {}