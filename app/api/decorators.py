from functools import wraps
from flask import abort
from flask.ext.login import current_user
from .errors import forbidden
from ..models import Role

def permission_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if current_user.role == Role.ADMIN:
                    pass
                elif not current_user.role == role:
                    return forbidden('Insufficient permissions')
            except: return forbidden('Insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator
