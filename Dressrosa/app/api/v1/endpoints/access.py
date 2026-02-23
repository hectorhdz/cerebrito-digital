"""Role-protected verification endpoints for API access control."""

from fastapi import APIRouter, Depends

from app.modules.auth.dependencies import require_api_roles

router = APIRouter(prefix="/access")


@router.get("/employee")
def employee_access(user=Depends(require_api_roles("employee"))) -> dict[str, str]:
    return {"message": f"Employee access granted to {user.username}"}


@router.get("/manager")
def manager_access(user=Depends(require_api_roles("manager"))) -> dict[str, str]:
    return {"message": f"Manager access granted to {user.username}"}


@router.get("/hr")
def hr_access(user=Depends(require_api_roles("hr"))) -> dict[str, str]:
    return {"message": f"HR access granted to {user.username}"}


@router.get("/admin")
def admin_access(user=Depends(require_api_roles("admin"))) -> dict[str, str]:
    return {"message": f"Admin access granted to {user.username}"}
