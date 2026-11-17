from django.urls import path

from authentication import views

urlpatterns = [
    path("signon/login", views.signon_login_view, name="signon_login"),
    path("oauth", views.oauth_callback_view, name="oauth_callback"),
    # path("logout", views.logout_view, name="logout"),
    # path("auth-error", views.auth_error_view, name="auth_error"),
]
