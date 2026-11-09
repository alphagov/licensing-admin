from models.local_authority import LocalAuthority
from playwright.sync_api import Page, expect

# Given for all tests
# - There is a GDS admin user set-up in the Signon mock


def test_has_title(page: Page, django_server: str) -> None:
    page.goto(django_server)
    expect(page).to_have_title("Hello World")


def test_gds_admin_can_view_all_authorities(page: Page, django_server: str, database_url: str) -> None:

    # Given: The database is populated with authorities
    test_authority = LocalAuthority(database_url, "Wakefield")
    test_authority.save_in_database()

    # When: We go to the login page and login successfully as the GDS admin user
    page.goto(django_server)
    page.get_by_test_id("login").click()

    # Then: The page that loads after sign-in should contain all the authorities from the database
    assert test_authority.is_equal_to_html_table_version(page.get_by_test_id("authorities").inner_html())
