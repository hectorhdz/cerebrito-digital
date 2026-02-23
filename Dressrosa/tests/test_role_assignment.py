"""Tests for BL-007 role assignment service wiring."""

from app.modules.users import service


def test_role_assignment_service_functions_exist() -> None:
    assert hasattr(service, "list_roles")
    assert hasattr(service, "assign_role_to_user")
    assert hasattr(service, "remove_role_from_user")
    assert hasattr(service, "get_user_role_names")
