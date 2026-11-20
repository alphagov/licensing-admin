from django.urls import path

from licensing_admin.views import authorities_list, login, oauth_callback_view, signon_login_view

urlpatterns = [
    path("login", login, name="login"),
    path("signon/login", signon_login_view, name="signon_login"),
    path("oauth", oauth_callback_view, name="oauth_callback"),
    path("authorities", authorities_list, name="authorities_list"),
]
