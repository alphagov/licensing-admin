from models.admin_app import AdminApp


def test_logged_in_user_that_logs_out_is_logged_out_from_app_and_signon(admin_app: AdminApp):
    # Given:
    # - User logged in
    user = admin_app.login_as_gds_superadmin()
    admin_app.verify_login_occurred_correctly(user)
    # When
    # - user signs out
    admin_app.log_out_current_user()

    # Then
    # - The users current session is cleared, and they're redirected to signon's sign out functionality
    # get current licensify user which either should be null or maybe anonymous user
    # assert the signon mock recieved a request to log the user out
    admin_app.verify_user_logged_out_correctly()
