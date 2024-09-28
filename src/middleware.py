import os

import jwt
from flask import current_app
from functools import wraps

from flask import request


def auth_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        current_app.logger.info("AUTH MIDDLEWARE | checking request")
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401

        try:
            data = jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
        except Exception as e:
            return {
                "message": "Unauthorized",
                "data": None,
                "error": str(e)
            }, 401

        kwargs["decoded"] = data
        return f(*args, **kwargs)
    return decorated