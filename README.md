# Licensing Admin
Licensing admin application to manage licence applications

## Set up

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
