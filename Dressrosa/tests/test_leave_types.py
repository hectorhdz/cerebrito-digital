"""Tests for BL-011 leave type management wiring."""

from app.api.v1.endpoints import leave_types
from app.modules.leaves import service


def test_leave_type_service_module_loads() -> None:
    assert hasattr(service, "create_leave_type")
    assert hasattr(service, "list_leave_types")
    assert hasattr(service, "update_leave_type")
    assert hasattr(service, "delete_leave_type")
    assert hasattr(service, "ensure_default_leave_types")


def test_leave_type_endpoint_module_loads() -> None:
    assert hasattr(leave_types, "api_list_leave_types")
    assert hasattr(leave_types, "api_create_leave_type")
    assert hasattr(leave_types, "api_get_leave_type")
    assert hasattr(leave_types, "api_update_leave_type")
    assert hasattr(leave_types, "api_delete_leave_type")
