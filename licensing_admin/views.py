from common.models.authority import Authority
from django.shortcuts import render


def login(request):
    return render(request, "licensing_admin/login_page.html", {"title": "Login  - Licensing - GOV.UK"})


def authorities_list(request):
    authorities = Authority.objects.all()
    return render(
        request,
        "licensing_admin/authorities_list_page.html",
        context={"title": "Authorities", "authorities": authorities},
    )
