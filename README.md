# Licensing Admin

Licensing admin application to manage licence applications

## Set up

### Environment Variables

- ADMIN_APP_AUTH_CODE_RESPONSE_URL
    - Specifies the URL that should be redirected to by GOV.UK Signon when an auth code request is submitted
- DJANGO_SECRET_KEY
- DOCUMENTDB_ALLOW_INVALID_CERTS = "true"
- DOCUMENTDB_IMAGE
    - Used by the `licensing_common` Git submodule to provide a DocumentDB service when running the system
      on a local machine
- DOCUMENTDB_PASSWORD
- DOCUMENTDB_PORT
- DOCUMENTDB_USER
- IS_PRODUCTION
- SESSION_COOKIE_AGE
    - Specified in seconds
- SIGNON_ACCESS_TOKEN_REQUEST_URL = ""
- SIGNON_AUTH_CODE_REQUEST_URL = ""
- SIGNON_CLIENT_ID
- SIGNON_CLIENT_SECRET = "dev-client-secret"
- SIGNON_LOGOUT_URL = ""
- SIGNON_USER_DETAILS_URL = ""

## Mise

This repository uses [mise](https://mise.jdx.dev/) to manage tool versions and environment variables.

After installing mise, you should set up your shell to automatically activate mise
following [these instructions](https://mise.jdx.dev/installing-mise.html#shell-specific-installation-activation), then
run `mise install` and `mise trust`.

## UV

This repository uses `uv` to manage packages and dependencies. Run `make prepare` to install all necessary packages and
dependencies needed
to test and run this project.

The python virtual environment should be automatically activated by mise. If it hasn't, run `source .venv/bin/activate`.

## Pre-Commit

This project uses `pre-commit`. Run `pre-commit install` to setup the correct pre-commit git hooks.

## Testing

**PLEASE ENSURE DOCKER DESKTOP OR ANOTHER CONTAINERISATION ENGINE IS RUNNING BEFORE RUNNING TESTS!**

Tests use [testcontainers](testcontainers.com) and [Playwright](https://playwright.dev/python/).

To run all tests execute `$ make test`.