from common.models.authority import Authority
from django.shortcuts import render

from authentication.decorators import public_view


@public_view
def login(request):
    return render(request, "licensing_admin/login_page.html")


@public_view  # TODO remove
def authorities_list(request):
    authorities = Authority.objects.all()
    return render(
        request,
        "licensing_admin/authorities_list_page.html",
        context={"authorities": authorities},
    )


def licences_list(request):
    # placeholder
    return render(
        request,
        "licensing_admin/authorities_list_page.html",
    )
