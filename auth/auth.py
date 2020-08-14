import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'moviehub.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'moviehub'
# AuthError Exception

'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

# soruce : https://github.com/udacity/FSND/blob/master/BasicFlaskAuth/app.py
def get_token_auth_header():

    # Obtains the Access Token from the Authorization Header
    header = request.headers.get('Authorization', None)

    cookie = request.cookies.get('jwt', None)

    # Check if the auth header is available
    if not header and not cookie:
        abort(401, 'Authorization header or cookie is expected.')

    auth = header if cookie is None else cookie

    # Check if it bearer or not
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        abort(401, 'Authorization header must start with "Bearer".')

    # Check if the Token is available
    elif len(parts) == 1:
        abort(401, 'Token not found.')

    # Check if the Token is bearer
    elif len(parts) > 2:
        abort(401, 'Authorization header must be bearer token.')

    token = parts[1]
    return token


def check_permissions(permission, payload):
    # Check if permissions array in the JWT
    if 'permissions' not in payload:
        abort(500, 'There is no permissions header in jwt')

    # Check if the user have permissions to accsses this rescuers
    if permission not in payload['permissions']:
        abort(401, 'Permission Not found')
    return True


# soruce : https://github.com/udacity/FSND/blob/master/BasicFlaskAuth/app.py
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        abort(401, 'Authorization malformed.')

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:

            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            abort(401, 'Token expired.')

        except jwt.JWTClaimsError:
            abort(401, 'Incorrect claims. Please, check the audience and issuer.')
        except Exception:
            abort(400, 'Unable to parse authentication token.')
            abort(400, 'Unable to find the appropriate key.')

# soruce : https://github.com/udacity/FSND/blob/master/BasicFlaskAuth/app.py


def requires_auth(permission=None):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            if permission is not None:
                check_permissions(permission, payload)
            payload['sub'] = payload['sub'][6:]
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
