from custom_assertions import assert_table_matches
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
    admin_app.navigate_to_authorities()
    # Then:
    assert "authorit" in admin_app.current_page_title().lower()
    assert_table_matches(
        admin_app,
        table_test_id="authorities",
        expected_objects=test_authorities,
        field_map={
            "Authority Full Name": "full_name",
            "Agency ID": "agency_id",
        },
    )


def test_unauthorised_user_is_redirected_to_login(admin_app: AdminApp):
    # Given:
    # - Not signed in

    # When:
    # - Try to navigate to a page

    admin_app.navigate_to_licences()

    # Then:
    # - Redirected to the login page
    assert "login" in admin_app.current_page_title().lower()


def test_authorised_user_in_broken_state_is_redirect_to_error_page():
    # Given:
    # - Signed in but permissions are "weird"

    # When:
    # - Try to navigate to a page

    # Then:
    # - Redirect to an error page
    pass
