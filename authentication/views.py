from django.views.decorators.http import require_GET

from authentication.decorators import public_view
from authentication.signon import handle_signon_callback, start_signon_redirect


@public_view
@require_GET
def signon_login_view(request):
    return start_signon_redirect(request)


@public_view
@require_GET
def oauth_callback_view(request):
    return handle_signon_callback(request)
