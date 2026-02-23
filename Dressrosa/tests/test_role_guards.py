"""Unit tests for role hierarchy and authorization helpers."""

from app.modules.auth.dependencies import expand_roles


def test_admin_inherits_all_roles() -> None:
    assert expand_roles({"admin"}) == {"admin", "hr", "manager", "employee"}


def test_hr_inherits_manager_and_employee() -> None:
    assert expand_roles({"hr"}) == {"hr", "manager", "employee"}


def test_manager_inherits_employee() -> None:
    assert expand_roles({"manager"}) == {"manager", "employee"}


def test_multiple_roles_expand_without_duplication() -> None:
    assert expand_roles({"employee", "manager"}) == {"employee", "manager"}
