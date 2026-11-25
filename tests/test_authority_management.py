from helpers.list_helpers import Column, extract_img_base64
from models.admin_app import AdminApp
from models.local_authority import LocalAuthorityFactory


def test_gds_admin_can_view_all_authorities(
    admin_app: AdminApp, local_authority_factory: LocalAuthorityFactory
) -> None:
    # Given:
    # - The database is populated with authorities
    test_authorities = local_authority_factory.create_x(10)

    # When:
    # - We login as a GDS superadmin user
    user = admin_app.login_as_gds_superadmin()

    # Then
    # - The user should be correctly logged into signon
    admin_app.verify_login_occurred_correctly(user)

    # - The authorised GDS admin can view a list of all authorities including name, payment provider, agencyID, logo
    columns = [
        Column(table_header="Authority Full Name", db_field_name="full_name"),
        Column(table_header="Payment Provider", db_field_name="payment_provider"),
        Column(table_header="Agency ID", db_field_name="agency_id"),
        Column(
            table_header="Logo",
            db_field_name="image_base_64_encoded",
            ui_data_mapping_function=extract_img_base64,
        ),
    ]
    admin_app.verify_admin_data_table_matches_expected_data(
        table_test_id="authorities", expected_objects=test_authorities, columns=columns
    )


def test_unauthorised_user_is_redirected_to_login(admin_app: AdminApp):
    # Given:
    # - Not signed in

    # When:
    # - Try to navigate to authorities page
    admin_app.navigate_to_authorities()

    # Then:
    # - Redirected to the login page
    assert "login" in admin_app.current_page_title().lower()


def test_authorised_user_without_gds_administrator_privileges_is_immediately_redirected(
    admin_app: AdminApp,
    local_authority_factory: LocalAuthorityFactory,
):
    # Given:
    # - Signed in as local authority for barnet and authority data exists
    user = admin_app.login_as_local_administrator_for_barnet()
    local_authority_factory.create_x(1)

    # When:
    # - Try to navigate to authorities page
    with admin_app.browser.expect_response(lambda res: "/authorities" in res.url) as response_info:
        admin_app.navigate_to_authorities()

    initial_response = response_info.value

    # Then:
    # - User is redirected without authority page ever returning data
    admin_app.verify_login_occurred_correctly(user)
    assert initial_response.status in (302, 303)
    assert "authorities" not in admin_app.browser.url


def test_logged_in_user_that_logs_out_is_logged_out_correctly(admin_app: AdminApp):
    # Given:
    # - User logged in as gds admin
    user = admin_app.login_as_gds_superadmin()

    # When
    # - The user signs out
    admin_app.log_out_current_user()

    # Then
    # - The user is no longer logged in to the system and has left authorities page
    admin_app.verify_user_logged_out_and_redirected_correctly(user)
