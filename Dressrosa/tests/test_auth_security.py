"""Unit tests for auth security utilities."""

from app.modules.auth.security import create_access_token, decode_access_token, hash_password, verify_password


def test_password_hash_and_verify_round_trip() -> None:
    password = "S3cure!123"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)


def test_access_token_contains_subject() -> None:
    token, expires_in = create_access_token("user-123")
    payload = decode_access_token(token)

    assert payload["sub"] == "user-123"
    assert expires_in == 7200
