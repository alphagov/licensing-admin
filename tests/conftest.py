from collections.abc import Generator, Iterator

import pytest
from models.admin_app import AdminApp
from models.gov_uk_signon_mock import GovUkSignonMock
from models.local_authority import LocalAuthorityFactory
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


@pytest.fixture
def admin_app(test_environment: DockerCompose, page: Page, govuk_signon_mock: GovUkSignonMock) -> AdminApp:
    return AdminApp(page, f"http://localhost:{test_environment.get_service_port('django', 8000)}", govuk_signon_mock)


@pytest.fixture(scope="session")
def govuk_signon_mock(test_environment: DockerCompose) -> GovUkSignonMock:
    return GovUkSignonMock("localhost", test_environment.get_service_port("mockserver", 1080))


@pytest.fixture(scope="session")
def local_authority_factory(test_environment: DockerCompose) -> Generator[LocalAuthorityFactory]:
    host_port = test_environment.get_service_port("document_db", 10260)
    db_url = f"mongodb://docdb:password@localhost:{host_port}/licensify?authSource=admin"
    with LocalAuthorityFactory(db_url) as factory:
        yield factory
