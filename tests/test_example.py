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
    assert "authorit" in admin_app.current_page_title().lower()
    columns = [
        Column("Authority Full Name", "full_name"),
        Column("Payment Provider", "payment_provider"),
        Column("Agency ID", "agency_id"),
        Column("Logo", "image_base_64_encoded", ui=extract_img_base64),
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
