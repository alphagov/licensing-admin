from models.admin_app import AdminApp


def test_unauthorised_user_is_redirected_to_login(admin_app: AdminApp):
    # Given:
    # - Not signed in

    # When:
    # - Try to navigate to authorities page
    admin_app.navigate_to_applications()

    # Then:
    # - Redirected to the login page
    assert "login" in admin_app.current_page_title().lower()
