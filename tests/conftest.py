from collections.abc import Iterator

import pytest
from playwright.sync_api import Page
from testcontainers.compose import DockerCompose


@pytest.fixture(autouse=True)
def set_playwright_timeout(page: Page):
    # Action timeout (click, fill, wait_for_selector, etc.) in milliseconds
    page.set_default_timeout(2000)


@pytest.fixture(scope="session")
def test_environment() -> Iterator[DockerCompose]:
    with DockerCompose(context="tests", compose_file_name="docker-compose.test.yml", wait=True, build=True) as compose:
        yield compose


@pytest.fixture(scope="session")
def django_server(test_environment: DockerCompose) -> str:
    return f"http://localhost:{test_environment.get_service_port('django', 8000)}"


@pytest.fixture(scope="session")
def login_page(test_environment: DockerCompose) -> str:
    return f"http://localhost:{test_environment.get_service_port('django', 8000)}/login"


@pytest.fixture(scope="session")
def authorities_page(test_environment: DockerCompose) -> str:
    return f"http://localhost:{test_environment.get_service_port('django', 8000)}/authorities"


@pytest.fixture(scope="session")
def govuk_signon_mock(test_environment: DockerCompose) -> str:
    return f"http://localhost:{test_environment.get_service_port('mockserver', 1080)}"


@pytest.fixture(scope="session", autouse=True)
def database_url(test_environment: DockerCompose) -> str:
    host_port = test_environment.get_service_port("document_db", 10260)
    return f"mongodb://docdb:password@localhost:{host_port}/core_data?authSource=admin"
