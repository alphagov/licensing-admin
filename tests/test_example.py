from playwright.sync_api import Page, expect


def test_has_title(page: Page, django_server: str) -> None:
    page.goto(django_server)
    expect(page).to_have_title("Hello World")
