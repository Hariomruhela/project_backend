from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from dependencies import get_current_admin

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"]
)

# -------------------------
# Get All Users
# -------------------------
@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):
    users = db.query(models.User).all()
    return users


# -------------------------
# Toggle Admin Role
# -------------------------
@router.put("/users/{user_id}/toggle-role")
def toggle_role(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # prevent admin changing themselves
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="You cannot change your own role")

    user.is_admin = not user.is_admin

    db.commit()
    db.refresh(user)

    return {
        "message": "Role updated",
        "is_admin": user.is_admin
    }


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin = Depends(get_current_admin)
):

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent admin deleting themselves
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="You cannot delete yourself")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}