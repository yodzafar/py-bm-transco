from asgiref.local import Local

_local = Local()

def set_current_user(user):
    _local.user = user

def get_current_user():
    return getattr(_local, 'user', None)

def clear_current_user():
    try:
        del _local.user
    except AttributeError:
        pass