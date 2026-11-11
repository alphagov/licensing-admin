from helpers.list_helper import extract_values_and_sort_result
from models.admin_app import AdminApp
from models.gov_uk_signon_mock import GovUkSignonMock
from models.local_authority import LocalAuthorityFactory


def test_has_title(admin_app: AdminApp) -> None:
    assert admin_app.current_page_title() == "Hello World"


def test_gds_admin_can_view_all_authorities(
    admin_app: AdminApp, local_authority_factory: LocalAuthorityFactory, govuk_signon_mock: GovUkSignonMock
) -> None:

    # Given:
    # - The database is populated with authorities
    test_authorities = local_authority_factory.create_x(5)

    # When:
    # - We login as a GDS superadmin user
    admin_app.login_as_gds_superadmin()
    admin_app.navigate_to("authorities")
    # Then:
    assert admin_app.current_page_title() == "Authorities"
    # - The page that loads after sign-in should contain all expected authority details
    authorities_rendered: list[dict[str, str]] = admin_app.convert_html_table_to_pythonic_data_structure("authorities")
    authority_names_rendered: list[str] = extract_values_and_sort_result(authorities_rendered, "name")
    test_authority_names: list[str] = extract_values_and_sort_result(test_authorities, "full_name")

    assert authority_names_rendered == test_authority_names


def test_unauthorised_user_is_redirected_to_login(admin_app: AdminApp):
    # Given:
    # - Not signed in

    # When:
    # Try to navigate to a page
    admin_app.navigate_to("authorities")

    # Then:
    # - Redirected to the login page
    assert admin_app.current_page_title() == "Login - Licensing - GOV.UK"


def test_authorised_user_in_broken_state_is_redirect_to_error_page():
    pass
