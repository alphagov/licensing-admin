from common.models.authority import Authority

# needed to stop it breaking when doing select_related("payment_account"))
from common.models.authority_payment_account import AuthorityPaymentAccount  # noqa: F401
from django.shortcuts import render

from authentication.decorators import public_view


@public_view
def login(request):
    return render(request, "licensing_admin/login_page.html")


def authorities_list(request):
    authorities = list(Authority.objects.select_related("payment_account"))

    return render(
        request,
        "licensing_admin/authorities_list_page.html",
        context={"authorities": authorities},
    )
