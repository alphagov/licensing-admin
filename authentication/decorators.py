from functools import wraps


def public_view(view_func):
    """Marks a view function as exempt from authentication and permission checks."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapper._is_public = True
    return wrapper
