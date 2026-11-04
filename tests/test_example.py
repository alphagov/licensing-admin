from playwright.sync_api import Page, expect


def test_has_title(page: Page, django_server: str) -> None:
    page.goto(django_server)
    expect(page).to_have_title("Hello World")


def gds_admin_can_view_all_authorities(page: Page, django_server: str) -> None:
    # Given
    # - The database is populated with authorities
    # - The database has a GDS admin user populated

    # When
    # - We go to the login page and login successfully as the GDS admin user
    page.goto(django_server)
    page.getByTestId("login").click()

    # Then
    # - The page that loads after sign-in should contain all the authorities from the database
