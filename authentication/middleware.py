from django.shortcuts import redirect

from authentication.licensify_user import AnonymousLicensifyUser, LicensifyUser


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

    def _home_redirect(self, request):
        if request.user.is_gds_admin:
            return redirect("authorities_list")
        if len(request.user.authorities) > 0:
            first_authority = next(iter(request.user.authorities))
            return redirect("applications_list", authority_slug=first_authority)
        return redirect("/login")

    def process_view(self, request, view_func, view_args, view_kwargs):
        if getattr(view_func, "_is_public", False):
            return None

        if not request.user.is_authenticated:
            return redirect("/login")

        is_gds_admin_view = getattr(view_func, "_is_gds_admin", False)
        is_local_authority_view = getattr(view_func, "_is_local_authority", False)

        if request.user.is_gds_admin:
            return None if is_gds_admin_view else self._home_redirect(request)

        if len(request.user.authorities) > 0:
            return None if is_local_authority_view else self._home_redirect(request)

        return redirect("/login")
