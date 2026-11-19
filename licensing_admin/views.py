from common.models.authority import Authority

# needed to stop it breaking when doing select_related("payment_account"))
from common.models.authority_payment_account import AuthorityPaymentAccount  # noqa: F401
from django.http import HttpRequest
from django.shortcuts import render
from django.views.decorators.http import require_GET

from authentication.decorators import public_view
from authentication.signon.signon_authorisation_code import SignonAuthorisationCode


@public_view
def login(request):
    return render(request, "licensing_admin/login_page.html")


@public_view
@require_GET
def signon_login_view(request: HttpRequest):
    return SignonAuthorisationCode.request(request)


@public_view
@require_GET
def oauth_callback_view(signon_auth_code_response):
    return (
        SignonAuthorisationCode(signon_auth_code_response)
        .exchange_for_signon_access_token()
        .retrieve_signon_user()
        .login()
    )


def authorities_list(request):
    authorities = list(Authority.objects.select_related("payment_account"))

    return render(
        request,
        "licensing_admin/authorities_list_page.html",
        context={"authorities": authorities},
    )
