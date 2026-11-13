from django.urls import path

from licensing_admin.views import authorities_list, licences_list, login

urlpatterns = [
    path("login", login, name="login"),
    path("authorities", authorities_list, name="authorities_list"),
    path("licences", licences_list, name="licences_list"),
]
