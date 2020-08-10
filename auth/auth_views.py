
from flask import Blueprint, request
import traceback
from flask_json import JsonError, as_json
from user.User import User
from .token_required import token_required
from .secret_key import SECRET_KEY
from .AuthError import AuthError

auth_views = Blueprint("user", __name__)


##Login

@auth_views.route('/login', methods=['POST'])
@as_json
def login():
    try:
        passed_credentials = request.get_json(force=True)
        selected_user = User.get(multiple = False, username=passed_credentials["username"])
        if selected_user is None:
            raise ValueError("Incorrect Username or password")
        token = selected_user.check_credentials(passed_credentials["password"], SECRET_KEY)
    except (KeyError, TypeError, ValueError, AuthError) as e:
        traceback.print_exc()
        User.rollback()

        raise JsonError(description=e.args[0])

    return token

@auth_views.route('/new_user', methods=['POST'])
@as_json
def new_user():
    try:
        passed_credentials = request.get_json(force=True)
        User.create(**passed_credentials)
    except (KeyError, TypeError, ValueError, AuthError) as e:
        traceback.print_exc()

        raise JsonError(description=e.args[0])

    return {}


@auth_views.route('/change_password', methods=['POST'])
@token_required
@as_json
def update_password(requesting_user):
    try:
        config = request.get_json(force=True)

        if "id" in config.keys():

            user_to_update = User.get_by_id(config["id"])

            if requesting_user.role_id <= user_to_update.role_id:
                raise AuthError("Not authorized to perfrom operation")

            user_to_update.change_password(config["new_password"])
            return {"id": user_to_update.id}

        else:
            ##Check old password
            requesting_user.check_credentials(config["old_password"], SECRET_KEY)

            requesting_user.change_password(config["new_password"])
            return

    except (KeyError, TypeError, ValueError) as e:
        traceback.print_exc()
        raise JsonError(description=e.args[0])