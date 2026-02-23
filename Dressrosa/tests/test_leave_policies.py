"""Tests for BL-013 leave policy placeholder wiring."""

from app.api.v1.endpoints import leave_policies
from app.modules.leaves import service


def test_leave_policy_service_module_loads() -> None:
    assert hasattr(service, "create_leave_policy")
    assert hasattr(service, "list_leave_policies")
    assert hasattr(service, "update_leave_policy")
    assert hasattr(service, "delete_leave_policy")
    assert hasattr(service, "ensure_default_leave_policies")


def test_leave_policy_endpoint_module_loads() -> None:
    assert hasattr(leave_policies, "api_list_leave_policies")
    assert hasattr(leave_policies, "api_create_leave_policy")
    assert hasattr(leave_policies, "api_get_leave_policy")
    assert hasattr(leave_policies, "api_update_leave_policy")
    assert hasattr(leave_policies, "api_delete_leave_policy")
