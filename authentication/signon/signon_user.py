import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect

from config import settings


class SignonUser:
    def __init__(self, access_token: str, request: HttpRequest):
        user_details_query = urlencode({"access_token": access_token})
        separator = "&" if "?" in settings.SIGNON_USER_DETAILS_URL else "?"
        signon_user_details_request = Request(
            f"{settings.SIGNON_USER_DETAILS_URL}{separator}{user_details_query}",
            headers={"Accept": "application/json"},
            method="GET",
        )
        with urlopen(signon_user_details_request, timeout=10) as user_response:
            user_data = json.loads(user_response.read().decode("utf-8"))

        self.user = user_data["user"]
        self.request = request

    def login(self) -> HttpResponseRedirect:
        # Rotate the session ID on login to prevent session fixation
        self.request.session.cycle_key()

        # This is essentially a login, the user details are now attached to
        # the Django request contexts moving forwards. The session key is used
        # by the auth middleware to create a LicensifyUser.
        self.request.session["signon_user"] = {
            "uid": self.user["uid"],
            "email": self.user["email"],
            "display_name": self.user["name"],
            "permissions": self._parse_signon_permissions(),
        }

        return redirect("authorities_list")

    def _parse_signon_permissions(self):
        # Signon returns permissions as either a flat list or a dict keyed by app name
        raw_perms = self.user.get("permissions", [])
        permissions = []
        if isinstance(raw_perms, dict):
            app_name = getattr(settings, "SIGNON_APP_NAME", "Licensify")
            permissions = raw_perms.get(app_name, [])
        else:
            permissions = list(raw_perms)

        return [p.lower() for p in permissions]
