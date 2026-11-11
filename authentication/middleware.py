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
            login_url = "/login"
            if request.path != login_url:
                return redirect(f"{login_url}")

        return self.get_response(request)
