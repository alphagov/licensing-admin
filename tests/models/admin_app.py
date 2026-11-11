from bs4 import BeautifulSoup
from playwright.sync_api import Page

from models.gov_uk_signon_mock import GovUkSignonMock


class AdminApp:
    def __init__(self, browser: Page, app_url: str, govuk_signon_mock: GovUkSignonMock):
        self.browser = browser
        self.app_url = app_url
        self.govuk_signon_mock = govuk_signon_mock
        self.browser.goto(app_url)

    def current_page_title(self) -> str:
        return self.browser.title()

    def convert_html_table_to_pythonic_data_structure(self, table_test_id: str) -> list[dict[str, str]]:
        """The table is returned so that each row is a list item,
        each column is a key in the dict, and the cell value is a
        value in the dict"""
        table_html = self.browser.get_by_test_id(table_test_id).inner_html()
        table = BeautifulSoup(table_html, "html.parser")
        headers = [th.get_text(strip=True) for th in table.select("thead th")]
        results = []
        for row in table.select("tbody tr"):
            cells = [td.get_text(strip=True) for td in row.select("td")]
            results.append(dict(zip(headers, cells, strict=True)))

        return results

    def login_as_gds_superadmin(self):
        self.govuk_signon_mock.mock_gds_superuser_login()
        self.browser.goto(f"{self.app_url}/login?")
        self.browser.get_by_test_id("login").click()

    def navigate_to(self, page: str):
        self.browser.goto(f"{self.app_url}/{page}")
