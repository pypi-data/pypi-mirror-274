import asyncio
import os
import tempfile
from collections.abc import Generator
from unittest.mock import patch

import pytest
from click.testing import CliRunner


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture(scope="session", autouse=True)
async def fixture_setup_env() -> None:
    session_mpatch = pytest.MonkeyPatch()
    session_mpatch.setenv("EXPONENT_API_KEY", "123456")
    session_mpatch.setenv("EXPONENT_BASE_URL", "https://exponent.run")
    session_mpatch.setenv("EXPONENT_API_BASE_URL", "https://api.exponent.run")


@pytest.fixture(scope="function")
def temporary_directory() -> Generator[str, None, None]:
    with tempfile.TemporaryDirectory() as test_directory:
        yield test_directory


@pytest.fixture(scope="function")
def default_temporary_directory(temporary_directory: str) -> Generator[str, None, None]:
    with open(os.path.join(temporary_directory, "test1.py"), "w") as f:
        f.write("print('Hello, world!')")

    with open(os.path.join(temporary_directory, "test2.py"), "w") as f:
        f.write("print('Hello, world!')")

    with open(os.path.join(temporary_directory, "exponent.txt"), "w") as f:
        f.write("Hello, world!")

    yield temporary_directory


@pytest.fixture(scope="function", autouse=True)
def mock_cli_heartbeat() -> Generator[None, None, None]:
    patcher = patch(
        "exponent.core.remote_execution.client.RemoteExecutionClient.send_heartbeat"
    )
    patcher.start()
    yield
    patcher.stop()
