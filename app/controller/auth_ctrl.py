import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from app.conf.db_config import DBConfig
from app.services.user_service import UserService
from app.util.pw_hash import verify_pw
from app.util.token_gen import create_access_token, create_refresh_token, verify_access_token, verify_refresh_token


router = APIRouter()
db = DBConfig()



@router.post('/login', description="로그인")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)):
    user = UserService.exisiting_user(form_data.username, db)  # ID로 사용자를 가져옴
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="존재하는 아이디가 없습니다.")

    if not verify_pw(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호 틀림")

    access_token = create_access_token(user.id)  # 토큰 생성
    refresh_token = create_refresh_token(user.id)
    try:
        UserService.update_refreshtoken(user.id, refresh_token, db)
        headers = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        return JSONResponse(content={"result": "로그인 성공"}, status_code=status.HTTP_200_OK, headers=headers)
    except Exception as e:
        print(f"Exception : {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="refresh 저장 실패")

@router.get('/refresh',description="Access 토큰 가져오기")
async def get_access_from_refresh(refresh_token: Annotated[str, Header()] ,db:Session=Depends(db.get_db)):
    id = verify_refresh_token(refresh_token)
    access_token = create_access_token(id)
    return JSONResponse(content={"result": "Create Access Token"}, status_code=status.HTTP_200_OK, headers={"access_token": access_token})

def get_id_from_token(credentials, db):
    try: 
        id = verify_access_token(credentials)
        if not UserService.exisiting_user(id, db):
            raise logging.warning("침략경보")
        return id   
    except Exception as e:
        print(f"{e}")
        raise 