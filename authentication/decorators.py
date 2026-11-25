from functools import wraps


def public_view(view_func):
    """Marks a view function as exempt from authentication and permission checks."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapper._is_public = True
    return wrapper


def local_authority_view(view_func):
    """Marks a view function as needing at least local authority permission."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapper._is_local_authority = True
    return wrapper


def gds_admin_view(view_func):
    """Marks a view as requiring GDS administrator permission."""

    @wraps(view_func)
    def wrapper(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapper._is_gds_admin = True
    return wrapper
