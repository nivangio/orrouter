from flask import request
import jwt
from datetime import datetime
from pytz import timezone
from functools import wraps
from auth.AuthError import AuthError
from user import User
from flask_json import JsonError, as_json
from .secret_key import SECRET_KEY

### Decorators

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"]

        if not token:
            raise AuthError("Missing Token")
            # raise ValueError("Token faltante")
        try:
            data = jwt.decode(token, SECRET_KEY)
            requesting_user = User.get_by_id(data["user_id"])
        except:
            raise AuthError("Token invalido")

        ##Error si el token esta expirado
        if datetime.utcnow().timestamp() > data["exp"]:
            raise AuthError("Expired Token")

        ##Error si la info del usuario cambio despues de la generacion del Token
        last_modified_utc = requesting_user.last_modified.replace(tzinfo=timezone('UTC'))
        if last_modified_utc.timestamp() > data["iat"]:
            raise AuthError("Expired Token")

        return f(requesting_user, *args, **kwargs)

    return decorated
