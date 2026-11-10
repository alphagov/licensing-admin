from models.gov_uk_signon_mock import GovUkSignonMock
from models.local_authority import LocalAuthorityFactory
from playwright.sync_api import Page, expect


def test_has_title(page: Page, django_server: str) -> None:
    page.goto(django_server)
    expect(page).to_have_title("Hello World")


def test_gds_admin_can_view_all_authorities(
    page: Page, django_server: str, local_authority_factory: LocalAuthorityFactory, govuk_signon_mock: GovUkSignonMock
) -> None:

    # Given:
    # - There is a GDS admin user available
    # - The database is populated with authorities
    govuk_signon_mock.mock_gds_superuser_login()
    test_authorities = local_authority_factory.create_x(5)

    # When:
    # - We go to the login page and login successfully as the GDS admin user
    page.goto(f"{django_server}/login")
    page.get_by_test_id("login").click()

    # Then:
    # - The GOVUK Signon Login page should have been navigated to
    # - The page that loads after sign-in should contain all the authorities from the database
    assert govuk_signon_mock.verify_login_page_navigated_to_x_times(1)
    for authority in test_authorities:
        assert authority.is_equal_to_html_table_version(page.get_by_test_id("authorities").inner_html())
