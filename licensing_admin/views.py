from django.shortcuts import render

# from common.models.authority import Authority


def login(request):
    return render(request, "licensing_admin/login_page.html")


def authorities_list(request):
    # authorities = Authority.objects.all()
    # print(authorities)
    return render(request, "licensing_admin/authorities_list_page.html")
