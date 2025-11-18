import pytest
from src.core.auth import hash_password, verify_password, create_access_token, decode_token


def test_hash_and_verify_password():
    plain = "mysecret"
    hashed = hash_password(plain)
    assert isinstance(hashed, str)
    assert verify_password(plain, hashed) is True
    assert verify_password("wrong", hashed) is False


def test_create_and_decode_token():
    sub = {"user_id": 123, "company_id": 1}
    token = create_access_token(sub)
    assert isinstance(token, str)
    payload = decode_token(token)
    assert payload.get("sub") == sub
    assert "exp" in payload and "iat" in payload
