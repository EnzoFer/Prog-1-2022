from .. import jwt
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps


def admin_required(fn):

    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()

        if claims ['rol'] == "admin":
            return fn(*args, **kwargs)

        else:
            return "Error, acceso solo para administradores", 403

    return wrapper


@jwt.user_identity_loader
def user_identity_lookup(user):
    print("User identity lookup")
    return user.id

@jwt.additional_claims_loader
def add_claims_to_access_token(user):
    print ("Add claims to access token")
    claims = {
        "rol": user.rol,
        "id": user.id,
        "email": user.email
    }
    return claims