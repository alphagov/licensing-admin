from collections.abc import Iterator

import pytest
from testcontainers.core.container import DockerContainer
from testcontainers.core.image import DockerImage
from testcontainers.core.wait_strategies import LogMessageWaitStrategy


@pytest.fixture(scope="session")
def django_server() -> Iterator[str]:
    with DockerImage(path=".", tag="hello-django-test") as image:
        with (
            DockerContainer(str(image))
            .with_exposed_ports(8000)
            .with_env("DJANGO_ALLOWED_HOSTS", "*")
            # PYTHONUNBUFFERED=1 is required for tests to run correctly. Without this,
            # Python can buffer stdout when it's running inside a container (the Django app
            # runs in a container during test runs) rather than an interactive terminal.
            # Therefore, the wait strategy for the Django docker container setup won't appear
            # and allow test setup to pass therefore, tests will fail.
            .with_env("PYTHONUNBUFFERED", "1")
            .waiting_for(LogMessageWaitStrategy("Quit the server with CONTROL-C").with_startup_timeout(10))
        ) as container:
            host = container.get_container_host_ip()
            port = container.get_exposed_port(8000)
            url = f"http://{host}:{port}/"

            yield url
