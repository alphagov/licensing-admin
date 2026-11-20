# Licensing Admin
Licensing admin application to manage licence applications

## Set up

### Environment Variables

| NAME | Description |
| ---- | ----------- |
| IS_PRODUCTION | Whether the application should be run in a production context
| DJANGO_SECRET_KEY = "django-insecure-)_*-zeg)shi6!y!lufkmy_g8&6%s!0pk=d1erm)rgbchgqfa($"
| DOCUMENTDB_USER = "docdb"
| DOCUMENTDB_PASSWORD = "MX78weVPvR7a7wyJ"
| DOCUMENTDB_PORT = "10260" # The port to bind to the documentDB endpoint to on your local machine
| DOCUMENTDB_IMAGE = "ghcr.io/documentdb/documentdb/documentdb-local@sha256:8c8a716e27f398b03c397424c4ddd901bddbc22b9f910b17096b0b246c7c9011" # pg17-0.114.0
| DOCUMENTDB_ALLOW_INVALID_CERTS = "true"
| SIGNON_CLIENT_ID = "dev-client-id"
| SIGNON_CLIENT_SECRET = "dev-client-secret"
| SIGNON_AUTH_CODE_REQUEST_URL = ""
| ADMIN_APP_AUTH_CODE_RESPONSE_URL = ""
| SIGNON_ACCESS_TOKEN_REQUEST_URL = ""
| SIGNON_USER_DETAILS_URL = ""
| SESSION_COOKIE_AGE = 2700

## Mise

This repository uses [mise](https://mise.jdx.dev/) to manage tool versions and environment variables.

After installing mise, you should set up your shell to automatically activate mise following [these instructions](https://mise.jdx.dev/installing-mise.html#shell-specific-installation-activation), then run `mise install` and `mise trust`.

## UV

This repository uses `uv` to manage packages and dependencies. Run `make prepare` to install all necessary packages and dependencies needed
to test and run this project.

The python virtual environment should be automatically activated by mise. If it hasn't, run `source .venv/bin/activate`.

## Pre-Commit

This project uses `pre-commit`. Run `pre-commit install` to setup the correct pre-commit git hooks.

## Testing

**PLEASE ENSURE DOCKER DESKTOP OR ANOTHER CONTAINERISATION ENGINE IS RUNNING BEFORE RUNNING TESTS!**

Tests use [testcontainers](testcontainers.com) and [Playwright](https://playwright.dev/python/).

To run all tests execute `$ make test`.
