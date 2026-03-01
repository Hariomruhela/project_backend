from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from utils.security import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# -------------------------
# Register Route
# -------------------------
@router.post("/register")
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):

    # Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password
    hashed_password = hash_password(user.password)

    # Create user
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        is_admin=user.is_admin if user.is_admin else False
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# -------------------------
# Login Route
# -------------------------
@router.post("/login", response_model=schemas.TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    # Here username = email
    db_user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {"user_id": db_user.id, "is_admin": db_user.is_admin}
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "is_admin": db_user.is_admin
    }