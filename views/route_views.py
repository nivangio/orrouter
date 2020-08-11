from flask import Blueprint, request
import traceback
from flask_json import JsonError, as_json
from routes.Route import Route
from auth import token_required

route_views = Blueprint("route_views", __name__)


@route_views.route('/create_route', methods=['POST'])
@token_required
@as_json
def create_route(requesting_user):
    config = request.get_json(force=True)
    try:
        config["user_id"] = requesting_user.id
        Route.create(**config)

    except Exception as e:
        traceback.print_exc()
        raise JsonError(description=e.args[0])

    return {}