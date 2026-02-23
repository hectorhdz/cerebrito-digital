"""Tests for BL-006 user CRUD service behavior."""

from app.modules.users import service


def test_user_service_module_loads() -> None:
    assert hasattr(service, "create_user")
    assert hasattr(service, "list_users")
    assert hasattr(service, "update_user")
    assert hasattr(service, "delete_user")
