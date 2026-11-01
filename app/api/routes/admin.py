from fastapi import APIRouter, Depends

from app.api.dependencies import require_admin
from app.domain.entities.user import User

router = APIRouter(tags=["Authorization"])


@router.get("/admin")
def admin_endpoint(current_user: User = Depends(require_admin)):
    return {
        "message": "Welcome, administrator",
        "email": current_user.email,
        "role": current_user.role,
    }