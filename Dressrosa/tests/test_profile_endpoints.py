"""Tests for BL-009 profile and account status endpoint wiring."""

from app.api.v1.endpoints import profile


def test_profile_endpoint_module_loads() -> None:
    assert hasattr(profile, "get_my_profile")
    assert hasattr(profile, "get_user_account_status")
    assert hasattr(profile, "update_user_account_status")
