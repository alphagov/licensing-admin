from operator import itemgetter

from bs4 import BeautifulSoup
from helpers.list_helpers import Column, extract_db_rows, normalize_ui_rows
from playwright.sync_api import Page

from models.gov_uk_signon_mock import GovUkSignonMock


class AdminApp:
    def __init__(self, browser: Page, app_url: str, govuk_signon_mock: GovUkSignonMock):
        self.browser = browser
        self.app_url = app_url
        self.govuk_signon_mock = govuk_signon_mock
        self.browser.goto(app_url)

    def verify_admin_data_table_matches_expected_data(
        self,
        table_test_id: str,
        expected_objects: list,
        columns: list[Column],
        sort_by: str = "",
    ) -> None:
        __tracebackhide__ = True

        if not columns:
            raise ValueError("columns cannot be empty")

        sort_key = sort_by or columns[0].header

        raw_ui_rows = self._convert_html_table_to_pythonic_data_structure(table_test_id)
        normalized_ui_rows = normalize_ui_rows(raw_ui_rows, columns)
        actual = sorted(normalized_ui_rows, key=itemgetter(sort_key))

        extracted_db_rows = extract_db_rows(expected_objects, columns)
        expected = sorted(extracted_db_rows, key=itemgetter(sort_key))

        assert actual == expected

    def current_page_title(self) -> str:
        return self.browser.title()

    def _convert_html_table_to_pythonic_data_structure(self, table_test_id: str) -> list[dict[str, str]]:
        """The table is returned so that each row is a list item,
        each column is a key in the dict, and the cell value is a
        value in the dict"""
        table_html = self.browser.get_by_test_id(table_test_id).inner_html()
        table = BeautifulSoup(table_html, "html.parser")
        headers = [th.get_text(strip=True) for th in table.select("thead th")]
        results = []
        for row in table.select("tbody tr"):
            cells = [
                td.get_text(strip=True) or td.decode_contents().strip()
                # second half largely so we can test logo images
                for td in row.select("td")
            ]
            results.append(dict(zip(headers, cells, strict=True)))

        return results

    def login_as_gds_superadmin(self):
        self.govuk_signon_mock.mock_gds_superuser_login()
        self.browser.goto(f"{self.app_url}/login")
        self.browser.get_by_test_id("login").click()
        self.browser.wait_for_url(f"{self.app_url}/authorities")

    def _navigate_to(self, page: str):
        self.browser.goto(f"{self.app_url}/{page}")

    def navigate_to_authorities(self):
        self._navigate_to("authorities")

    def navigate_to_licences(self):
        self._navigate_to("licences")
