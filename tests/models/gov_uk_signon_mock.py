import json

from faker import Faker
from mockserver import HttpRequest, HttpResponse, HttpTemplate, MockServerClient

fake = Faker("en_GB")


class GovUkSignonMock:
    def __init__(self, host: str, port: int):
        self.client = MockServerClient(host, port)
        self.authorize_request = HttpRequest.request("/oauth/authorize").with_method("GET")
        self.token_request = HttpRequest.request("/oauth/token").with_method("POST")
        self.user_details_request = HttpRequest.request("/user.json").with_method("GET")
        self.logout_request = HttpRequest.request("/users/sign_out").with_method("GET")

    def mock_gds_superuser_login(self):
        return self._mock_user_login(permissions={"Licensify": ["signin", "gdsadministrator"]})

    def mock_local_authority_for_barnet(self):
        return self._mock_user_login(permissions={"Licensify": ["signin", "barnet"]})

    def verify_signon_login_occurred_correctly(self):
        auth_code_requests = self.client.retrieve_recorded_requests(self.authorize_request)
        access_token_requests = self.client.retrieve_recorded_requests(self.token_request)
        signon_user_data_requests = self.client.retrieve_recorded_requests(self.user_details_request)
        assert len(auth_code_requests) == 1
        assert len(access_token_requests) == 1
        assert len(signon_user_data_requests) == 1

    def verify_signon_logout_called(self):
        assert len(self.client.retrieve_recorded_requests(self.logout_request)) == 1

    def _mock_user_login(self, permissions: dict[str, list[str]] | list[str]):
        self._reset()

        user = {
            "user": {
                "uid": str(fake.uuid4()),
                "name": fake.name(),
                "email": fake.email(),
                "permissions": permissions,
            }
        }

        # 1. Browser hits /oauth/authorize -> 302 redirect back to Django's redirect_uri
        #    echoing the exact CSRF `state` query param plus a dummy auth `code`.
        redirect_location = (
            "$!request.queryStringParameters.get('redirect_uri').get(0)"
            "?code=test-auth-code"
            "&state=$!request.queryStringParameters.get('state').get(0)"
        )

        velocity_template = json.dumps(
            {
                "statusCode": 302,
                "headers": {
                    "Location": [redirect_location],
                },
            }
        )
        self.client.when(self.authorize_request).respond(
            HttpTemplate(
                template=velocity_template,
                template_type="VELOCITY",
            )
        )

        # 2. Django exchanges the code for an access token
        self.client.when(self.token_request).respond(
            HttpResponse.response(
                status_code=200,
                body=json.dumps(
                    {
                        "access_token": "test-access-token",
                        "token_type": "bearer",
                    }
                ),
            ).with_header("Content-Type", "application/json")
        )

        # 3. Django fetches the user's Signon profile & permissions
        self.client.when(self.user_details_request).respond(
            HttpResponse.response(
                status_code=200,
                body=json.dumps(user),
            ).with_header("Content-Type", "application/json")
        )

        return user

    def _reset(self):
        self.client.reset()
