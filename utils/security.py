from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status

# -------------------------
# Configurations
# -------------------------
SECRET_KEY = "your_secret_key_here"   # change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30      # Fixed: was 1 min (too short)
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------
# Password Hashing
# -------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------
# Create JWT Tokens
# -------------------------
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# -------------------------
# Decode JWT Tokens
# -------------------------
def decode_access_token(token: str) -> dict | None:
    """Decodes and validates an access token. Returns payload or None."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "access":
            return None  # Reject if someone passes a refresh token here
        return payload
    except JWTError:
        return None


def decode_refresh_token(token: str) -> dict | None:
    """Decodes and validates a refresh token. Returns payload or None."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            return None  # Reject if someone passes an access token here
        return payload
    except JWTError:
        return None


# -------------------------
# FastAPI Dependency: Protect Routes
# -------------------------
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """FastAPI dependency to protect routes. Use with Depends()."""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


# -------------------------
# Example Router (optional, shows usage)
# -------------------------
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


# Fake DB for demonstration — replace with your real DB logic
FAKE_USER_DB = {
    "testuser": {
        "username": "testuser",
        "hashed_password": hash_password("testpass123"),
    }
}


@router.post("/login")
def login(request: LoginRequest):
    """Login and receive access + refresh tokens."""
    user = FAKE_USER_DB.get(request.username)
    if not user or not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    access_token = create_access_token(data={"sub": request.username})
    refresh_token = create_refresh_token(data={"sub": request.username})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh")
def refresh(request: RefreshRequest):
    """Use a valid refresh token to get a new access token."""
    payload = decode_refresh_token(request.refresh_token)  # ✅ correct decoder
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    new_access_token = create_access_token(data={"sub": payload["sub"]})
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }


@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    """Protected route — returns current user info from token."""
    return {"username": current_user.get("sub")}