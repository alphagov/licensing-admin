import json
import logging
import secrets
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from authentication.models import SPECIAL_PERMISSIONS

logger = logging.getLogger(__name__)


def _get_callback_url(request) -> str:
    return settings.OAUTH_CALLBACK_URL_OVERRIDE or request.build_absolute_uri(reverse("oauth_callback"))


def start_signon_redirect(request):
    """Stores a random state token in the session and redirects to GOV.UK Signon."""
    state = secrets.token_urlsafe(32)
    request.session["oauth_state"] = state

    query = urlencode(
        {
            "client_id": settings.SIGNON_CLIENT_ID,
            "redirect_uri": _get_callback_url(request),
            "response_type": "code",
            "state": state,
        }
    )
    return redirect(f"{settings.SIGNON_AUTHORIZATION_URL}?{query}")


def handle_signon_callback(request):
    """Validates OAuth state, exchanges the code for user details, and completes login."""
    expected_state = request.session.pop("oauth_state", None)
    returned_state = request.GET.get("state", "")

    if not expected_state or not secrets.compare_digest(expected_state, returned_state):
        logger.warning("Signon OAuth state mismatch")
        request.session.flush()
        return redirect("login")

    user_data = _fetch_signon_user(
        code=request.GET["code"],
        callback_url=_get_callback_url(request),
    )
    return _complete_login(request, user_data)


def _fetch_signon_user(code: str, callback_url: str) -> dict:
    """Exchanges an authorization code for an access token and fetches the Signon profile."""
    token_payload = urlencode(
        {
            "client_id": settings.SIGNON_CLIENT_ID,
            "client_secret": settings.SIGNON_CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": callback_url,
        }
    ).encode("utf-8")

    token_request = Request(
        settings.SIGNON_ACCESS_TOKEN_URL,
        data=token_payload,
        headers={"Accept": "application/json"},
        method="POST",
    )
    with urlopen(token_request, timeout=10) as token_response:
        token_data = json.loads(token_response.read().decode("utf-8"))

    user_profile_access_token = token_data["access_token"]

    user_details_query = urlencode({"access_token": user_profile_access_token})
    separator = "&" if "?" in settings.SIGNON_USER_DETAILS_URL else "?"
    user_request = Request(
        f"{settings.SIGNON_USER_DETAILS_URL}{separator}{user_details_query}",
        headers={"Accept": "application/json"},
        method="GET",
    )
    with urlopen(user_request, timeout=10) as user_response:
        user_data = json.loads(user_response.read().decode("utf-8"))

    user = user_data["user"]

    # Signon returns permissions as either a flat list or a dict keyed by app name
    raw_perms = user.get("permissions", [])
    if isinstance(raw_perms, dict):
        app_name = getattr(settings, "SIGNON_APP_NAME", "Licensify")
        flat_perms = raw_perms.get(app_name, [])
    else:
        flat_perms = list(raw_perms)

    return {
        "uid": user["uid"],
        "email": user["email"],
        "display_name": user["name"],
        "permissions": [p.lower() for p in flat_perms],
    }


def _complete_login(request, user_data: dict):
    """Stores the verified Signon user in the session and redirects to their landing page."""
    permissions = [p.lower() for p in user_data.get("permissions", [])]
    authorities = [p for p in permissions if p not in SPECIAL_PERMISSIONS]

    if "signin" not in permissions:
        request.session.flush()
        return redirect("login")

    if "gdsadministrator" not in permissions and not authorities:
        request.session.flush()
        return redirect(f"{reverse('login')}?reason=no_authority")

    # Rotate the session ID on login to prevent session fixation
    request.session.cycle_key()
    request.session["signon_user"] = {
        "uid": user_data["uid"],
        "email": user_data["email"],
        "display_name": user_data["display_name"],
        "permissions": permissions,
    }

    # if "gdsadministrator" not in permissions:
    #     return redirect("applications", authority_slug=authorities[0])

    return redirect("authorities_list")
