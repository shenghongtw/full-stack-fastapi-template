from datetime import timedelta
from typing import Annotated, Any
import jwt
import requests

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.models import Message, NewPassword, Token, UserPublic, GoogleLogin, User, UserCreate
# from app.utils import (
#     generate_password_reset_token,
#     generate_reset_password_email,
#     send_email,
#     verify_password_reset_token,
# )

router = APIRouter(tags=["login"])

async def verify_google_token(token: str) -> dict:
    try:
        # 验证 Google ID token
        google_response = requests.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        )
        if google_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid Google token")
        return google_response.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login/google")
async def google_login(
    google_data: GoogleLogin,
    session: SessionDep,
) -> Token:
    """
    Google OAuth login
    """
    # 验证 Google token
    google_user = await verify_google_token(google_data.credential)
    
    # 检查用户是否已存在
    user = crud.get_user_by_email(session=session, email=google_user["email"])
    
    if not user:
        # 创建新用户
        user_in = UserCreate(
            email=google_user["email"],
            full_name=google_user.get("name"),
            is_active=True,
            google_id=google_user["sub"]
        )
        user = crud.create_user(session=session, user_create=user_in)
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.post("/login/test-token", response_model=UserPublic)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user
