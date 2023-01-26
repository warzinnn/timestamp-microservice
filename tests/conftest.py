import pytest

from app import create_app

"""
Fixtures for api testing
"""


@pytest.fixture()
def app():
    app = create_app()
    app.config.from_object("config.TestingConfig")
    print(f"Testing: {app.config['TESTING']}")
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
