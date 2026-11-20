import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.http import HttpRequest

from authentication.signon.signon_user import SignonUser
from config import settings


class SignonAccessToken:
    def __init__(self, authorisation_code: str, authorisation_code_redirect_uri: str, request: HttpRequest):
        token_request = Request(
            settings.SIGNON_ACCESS_TOKEN_REQUEST_URL,
            data=urlencode(
                {
                    "client_id": settings.SIGNON_CLIENT_ID,
                    "client_secret": settings.SIGNON_CLIENT_SECRET,
                    "grant_type": "authorization_code",
                    "code": authorisation_code,
                    # The redirect_uri is only used for validation by Signon: it should
                    # match the authorisation code redirect_uri sent previously.
                    "redirect_uri": authorisation_code_redirect_uri,
                }
            ).encode("utf-8"),
            headers={"Accept": "application/json"},
            method="POST",
        )
        with urlopen(token_request, timeout=10) as token_response:
            token_data = json.loads(token_response.read().decode("utf-8"))

        self.access_token = token_data["access_token"]
        self.request = request

    def retrieve_signon_user(self):
        return SignonUser(self.access_token, self.request)
