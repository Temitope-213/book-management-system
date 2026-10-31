from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import JWT_SECRET_KEY
from tests.conftest import PASSWORD


def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={"username": "maria", "email": "maria@example.com", "password": PASSWORD},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "maria@example.com"
    assert "password" not in body
    assert "password_hash" not in body


def test_register_ignores_role_and_defaults_to_user(client, user_repo):
    client.post(
        "/auth/register",
        json={
            "username": "sneaky",
            "email": "sneaky@example.com",
            "password": PASSWORD,
            "role": "admin",
        },
    )
    assert user_repo.get_by_email("sneaky@example.com").role == "user"


def test_register_duplicate_email(client):
    data = {"username": "maria", "email": "maria@example.com", "password": PASSWORD}
    client.post("/auth/register", json=data)
    response = client.post("/auth/register", json=data)
    assert response.status_code == 409


def test_register_invalid_input(client):
    response = client.post(
        "/auth/register",
        json={"username": "maria", "email": "maria@example.com", "password": "x"},
    )
    assert response.status_code == 422


def test_password_is_hashed(client, user_repo):
    client.post(
        "/auth/register",
        json={"username": "maria", "email": "maria@example.com", "password": PASSWORD},
    )
    stored = user_repo.get_by_email("maria@example.com")
    assert stored.password_hash != PASSWORD


def test_login_success_returns_token(client):
    client.post(
        "/auth/register",
        json={"username": "maria", "email": "maria@example.com", "password": PASSWORD},
    )
    response = client.post(
        "/auth/login", json={"email": "maria@example.com", "password": PASSWORD}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={"username": "maria", "email": "maria@example.com", "password": PASSWORD},
    )
    response = client.post(
        "/auth/login", json={"email": "maria@example.com", "password": "WrongPass999!"}
    )
    assert response.status_code == 401


def test_login_unknown_email_gives_same_error(client):
    response = client.post(
        "/auth/login", json={"email": "nobody@example.com", "password": PASSWORD}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_me_with_token(client, user_headers):
    response = client.get("/auth/me", headers=user_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"


def test_me_without_token(client):
    assert client.get("/auth/me").status_code == 401


def test_me_with_invalid_token(client):
    response = client.get("/auth/me", headers={"Authorization": "Bearer abc123"})
    assert response.status_code == 401


def test_me_with_expired_token(client, user_headers):
    expired_token = jwt.encode(
        {"sub": "1", "exp": datetime.now(timezone.utc) - timedelta(minutes=5)},
        JWT_SECRET_KEY,
        algorithm="HS256",
    )
    response = client.get(
        "/auth/me", headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401


def test_admin_endpoint_denied_for_user(client, user_headers):
    assert client.get("/admin", headers=user_headers).status_code == 403


def test_admin_endpoint_allowed_for_admin(client, admin_headers):
    assert client.get("/admin", headers=admin_headers).status_code == 200


def test_admin_endpoint_without_token(client):
    assert client.get("/admin").status_code == 401