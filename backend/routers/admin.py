from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from configs.config import ACCESS_TOKEN_EXPIRE_MINUTES
from dependencies import (
    Token,
    User,
    authenticate_user,
    create_access_token,
    fake_users_db,
    get_current_user,
)

router = APIRouter()


# 用户登录，获取token
@router.post("/admin/login", response_model=Token)
async def get_login_data(user: User):
    print(user)
    form_data = OAuth2PasswordRequestForm(
        username=user.username, password=user.password
    )
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return JSONResponse(
        {
            "msg": "ok",
            "code": 0,
            "data": {"username": user.username, "token": access_token},
        }
    )


# 获取用户信息
@router.get("/admin/info", response_model=User)
async def get_admin_info(current_user: User = Depends(get_current_user)):
    return JSONResponse(
        {
            "msg": "ok",
            "code": 0,
            "data": {
                "admin_info": {
                    "id": current_user.id,
                    "username": current_user.username,
                    "email": current_user.email,
                }
            },
        }
    )
