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


def test_logged_in_user_that_logs_out_is_logged_out_correctly(admin_app: AdminApp):
    # Given:
    # - User logged in
    user = admin_app.login_as_local_administrator_for_barnet()
    admin_app.verify_login_occurred_correctly(user)
    # When
    # - The user signs out
    admin_app.log_out_current_user()

    # Then
    # - The user is no longer logged in to the system and has left  the applications page
    admin_app.verify_user_logged_out_and_redirected_correctly(user)
