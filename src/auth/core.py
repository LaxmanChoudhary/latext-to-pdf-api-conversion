import datetime

import jwt


def create_jwt(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "expiration": (datetime.datetime.utcnow() + datetime.timedelta(days=1)).timestamp(),
            "iat": datetime.datetime.utcnow().timestamp(),
            "admin": authz
        },
        secret,
        algorithm="HS256",
    )
