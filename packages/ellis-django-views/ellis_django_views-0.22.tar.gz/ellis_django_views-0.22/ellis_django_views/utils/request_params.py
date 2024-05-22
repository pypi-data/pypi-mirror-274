from ellis_django_views.utils import error_messages

AUTH_TOKEN = 'HTTP_AUTHORIZATION'
PK = 'pk'
URL = 'url'
ID = 'id'
IMAGE = 'image'
CONTENT_TYPE = 'application/json'

def getBearer(auth_token):
    return f'Token {auth_token}'

def get_request_param_value(request, key):
    value = request.data.get(key)
    if value is not None:
        return value
    raise ValueError(f'{error_messages.MISSING_PARAMETER}{key}')

def get_request_header_param_value(request, key):
    value = request.META.get(key)
    if value is not None:
        return value
    raise ValueError(f'{error_messages.MISSING_HEADER_PARAMETER}{key}')