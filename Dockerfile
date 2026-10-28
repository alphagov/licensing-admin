FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# PYTHONUNBUFFERED=1 is required for tests to run correctly. Without this,
# Python can buffer stdout when it's running inside a container (the Django app
# runs in a container during test runs) rather than an interactive terminal.
# Therefore, the wait strategy for the Django docker container setup won't appear
# and allow test setup to pass therefore, tests will fail.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]