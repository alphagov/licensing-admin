import json

from faker import Faker
from mockserver import HttpRequest, HttpResponse, MockServerClient

fake = Faker("en_GB")


class GovUkSignonMock:
    def __init__(self, host: str, port: int):
        self.client = MockServerClient(host, port)
        self.login_request = HttpRequest.request("/signon/login").with_method("GET")

    def mock_gds_superuser_login(self):
        self.client.when(self.login_request).respond(
            HttpResponse.response(
                status_code=200,
                body=json.dumps(
                    {
                        "user": {
                            "uid": str(fake.uuid4()),
                            "name": fake.name(),
                            "email": fake.email(),
                            "permissions": {"Licensify": ["signin"]},
                        }
                    }
                ),
            )
        )

    def verify_login_page_navigated_to_x_times(self, x: int) -> bool:
        requests = self.client.retrieve_recorded_requests(self.login_request)

        return len(requests) == x
