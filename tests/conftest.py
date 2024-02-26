from typing import Generator

import pytest
from flask.testing import FlaskClient, FlaskCliRunner

from ctff import CTFF
from example import app as example_app_instance


@pytest.fixture
def example_app() -> Generator[CTFF, None, None]:
    yield example_app_instance


@pytest.fixture
def client(example_app: CTFF) -> FlaskClient:
    return example_app.test_client()


@pytest.fixture
def runner(example_app: CTFF) -> FlaskCliRunner:
    return example_app.test_cli_runner()
