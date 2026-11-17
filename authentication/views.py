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


# @public_view
# @require_GET
# def logout_view(request):
#     # Wipes the session data and deletes the sessionid cookie in the browser
#     request.session.flush()
#     return redirect(f"{settings.SIGNON_URL.rstrip('/')}/users/sign_out")


# @public_view
# @require_GET
# def auth_error_view(request):
#     reason = request.GET.get("reason", "unknown")
#     return render(
#         request,
#         "authentication/error.html",
#         {"reason": reason},
#         status=403,
#     )
