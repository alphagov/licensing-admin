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
            .waiting_for(LogMessageWaitStrategy("Quit the server with CONTROL-C").with_startup_timeout(10))
        ) as container:
            host = container.get_container_host_ip()
            port = container.get_exposed_port(8000)
            url = f"http://{host}:{port}/"

            yield url
