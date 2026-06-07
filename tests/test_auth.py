from tests.conftest import client


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "email": "testuser@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"


def test_duplicate_register_fails():
    client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password456"
        }
    )

    assert response.status_code == 400


def test_login_user():
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_current_user():
    client.post(
        "/auth/register",
        json={
            "email": "me@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": "me@example.com",
            "password": "password123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"