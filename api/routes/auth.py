# api/routes/auth.py
"""
Authentication Endpoints: Register, Login, Current User Profile.
"""

import uuid
from fastapi import APIRouter, HTTPException, Depends, status
from db.models import UserRegisterRequest, UserLoginRequest, TokenResponse
from db.storage import create_account, get_account_by_username, get_account_by_id
from api.middleware import hash_password, verify_password, create_access_token, get_current_user_id

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
async def register(req: UserRegisterRequest):
    existing = await get_account_by_username(req.username.strip())
    if existing:
        raise HTTPException(status_code=400, detail="Username is already registered")

    user_id = str(uuid.uuid4())[:8]
    pwd_hash = hash_password(req.password)
    
    success = await create_account(
        user_id=user_id,
        username=req.username.strip(),
        password_hash=pwd_hash,
        email=req.email.strip() if req.email else None
    )
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create user account")

    token = create_access_token({"sub": user_id, "username": req.username.strip()})
    return TokenResponse(
        access_token=token,
        user_id=user_id,
        username=req.username.strip()
    )


@router.post("/login", response_model=TokenResponse)
async def login(req: UserLoginRequest):
    account = await get_account_by_username(req.username.strip())
    if not account or not verify_password(req.password, account["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": account["user_id"], "username": account["username"]})
    return TokenResponse(
        access_token=token,
        user_id=account["user_id"],
        username=account["username"]
    )


@router.get("/me")
async def get_me(user_id: str = Depends(get_current_user_id)):
    account = await get_account_by_id(user_id)
    if not account:
        raise HTTPException(status_code=404, detail="User account not found")
    return {
        "user_id": account["user_id"],
        "username": account["username"],
        "email": account.get("email"),
        "created_at": account["created_at"]
    }
