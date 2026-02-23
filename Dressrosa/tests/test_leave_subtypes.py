"""Tests for BL-012 leave subtype management wiring."""

from app.api.v1.endpoints import leave_subtypes
from app.modules.leaves import service


def test_leave_subtype_service_module_loads() -> None:
    assert hasattr(service, "create_leave_subtype")
    assert hasattr(service, "list_leave_subtypes")
    assert hasattr(service, "update_leave_subtype")
    assert hasattr(service, "delete_leave_subtype")
    assert hasattr(service, "ensure_default_leave_subtypes")


def test_leave_subtype_endpoint_module_loads() -> None:
    assert hasattr(leave_subtypes, "api_list_leave_subtypes")
    assert hasattr(leave_subtypes, "api_create_leave_subtype")
    assert hasattr(leave_subtypes, "api_get_leave_subtype")
    assert hasattr(leave_subtypes, "api_update_leave_subtype")
    assert hasattr(leave_subtypes, "api_delete_leave_subtype")
