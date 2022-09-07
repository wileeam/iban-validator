import pytest

from app import create_app
from model.iban import Iban


@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_root(client):
    response = client.get("/")

    assert response.status_code == 302 or response.status_code == 200


def test_invalid_endpoint(client):
    response = client.get("/whatever")

    assert response.status_code == 404


def test_get_validate_no_account(client):
    response = client.get("/validate")

    assert response.status_code >= 400
    assert "error" in response.get_json()


def test_get_validate_account(client):
    accounts = [
        {"MC793903645089C80JGA29MY747": "OK"},
        {"QQ29VHAV322929767755897869423": "NOTOK"},
        {"LU608781YS8E20B1G520": "OK"},
        {"TA14873287923531987386761412": "NOTOK"},
        {"SE1244572683153012814280": "OK"},
        {"GZ96BARC20038445256154": "NOTOK"},
    ]

    for account in accounts:
        account_key = list(account.keys())[0]
        account_value = list(account.values())[0]

        response = client.get(
            "/validate", query_string={"account": account_key}
        )
        data = response.get_json()

        assert response.status_code == 200
        assert account_key in data and data[account_key] == account_value


def test_post_validate_no_account(client):
    response = client.post("/validate")

    assert response.status_code >= 400
    assert "error" in response.get_json()
