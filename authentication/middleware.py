from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from authentication.models import AnonymousLicensifyUser, LicensifyUser


class LicensifyAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_dict = request.session.get("signon_user")

        if user_dict:
            request.user = LicensifyUser(
                uid=user_dict["uid"],
                email=user_dict["email"],
                display_name=user_dict["display_name"],
                # Freeze the permissions array into an immutable tuple:
                permissions=tuple(user_dict.get("permissions", [])),
            )
        else:
            request.user = AnonymousLicensifyUser()

        return self.get_response(request)


class ViewPermissionEnforcementMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Exempt public views (marked with @public_view) - notably the login page or the callback from login
        login_url = "/login"
        if getattr(view_func, "_is_public", False):
            return None

        if not request.user.is_authenticated:
            if request.path != login_url:
                return redirect(f"{login_url}")

        if "authority_slug" in view_kwargs:
            slug = view_kwargs["authority_slug"]
            if not request.user.can_access_authority(slug):
                raise PermissionDenied(f"Access denied for authority '{slug}'.")
            return None

        if not request.user.is_gds_admin and not login_url:
            raise PermissionDenied("GDS Administrator access required.")

        return None
