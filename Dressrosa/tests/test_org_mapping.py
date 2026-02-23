"""Tests for BL-008 org mapping service wiring."""

from app.modules.users import service


def test_manager_mapping_service_functions_exist() -> None:
    assert hasattr(service, "assign_manager_to_user")
    assert hasattr(service, "ManagerAssignmentError")
