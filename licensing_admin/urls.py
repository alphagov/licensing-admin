from django.urls import path

from licensing_admin.views import authorities_list, login, logout, oauth_callback, signon_login

urlpatterns = [
    path("login", login, name="login"),
    path("logout", logout, name="logout"),
    path("signon/login", signon_login, name="signon_login"),
    path("oauth", oauth_callback, name="oauth_callback"),
    path("authorities", authorities_list, name="authorities_list"),
]
