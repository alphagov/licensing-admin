import logging
import secrets
from urllib.parse import parse_qsl, urlencode

from django.http import HttpRequest
from django.shortcuts import redirect

from authentication.signon.signon_access_token import SignonAccessToken
from config import settings

logger = logging.getLogger(__name__)


class SignonAuthorisationCode:
    def request(request: HttpRequest):
        """Stores a random state token in the session and redirects to GOV.UK Signon."""
        request.session["query"] = urlencode(
            {
                "client_id": settings.SIGNON_CLIENT_ID,
                "redirect_uri": settings.ADMIN_APP_AUTH_CODE_RESPONSE_URL,
                "response_type": "code",
                "state": secrets.token_urlsafe(32),
            }
        )
        return redirect(f"{settings.SIGNON_AUTH_CODE_REQUEST_URL}?{request.session['query']}")

    def __init__(self, auth_code_request_response: HttpRequest):
        self.auth_code_request_response = auth_code_request_response

    def exchange_for_signon_access_token(self):
        # Remove the query that was set in the access code request since we
        # no longer need it, and return its contents for use here
        initial_query = dict(parse_qsl(self.auth_code_request_response.session.pop("query", None)))

        if self._authentication_code_response_is_valid(initial_query):
            return SignonAccessToken(
                self.auth_code_request_response.GET["code"],
                initial_query.get("redirect_uri"),
                self.auth_code_request_response,
            )

        logger.warning("Signon OAuth state mismatch")
        self.auth_code_request_response.session.flush()
        return redirect("login")

    def _authentication_code_response_is_valid(self, initial_query: dict) -> bool:
        expected_state = initial_query.get("state", "")
        returned_state = self.auth_code_request_response.GET.get("state", "")

        return bool(expected_state and secrets.compare_digest(expected_state, returned_state))
