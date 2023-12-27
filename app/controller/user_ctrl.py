from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette import status
from sqlalchemy.orm import Session
from app.services.user_service import UserService

from app.conf.db_config import DBConfig

from app.models.api_model import CreateUser
from app.util.pw_hash import get_hashed_pw
from app.util.token_gen import create_access_token

router = APIRouter()
db = DBConfig()


@router.post('/', description="유저 생성")
async def user_create(user: CreateUser,  db: Session = Depends(db.get_db)):
    # ID 체크
    existing_user = UserService.exisiting_user(user.ID, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="ID Duplicated")
    new_user = {
        'ID': user.ID,
        'PASSWORD': get_hashed_pw(user.PASSWORD),
    }
    try:
        result = UserService.create_user(new_user, db)
        headers = {'access_token': create_access_token(new_user), 'refresh_token': result.refreshtoken}
        return JSONResponse(content={'code': status.HTTP_201_CREATED,
                            'result': f'Success to Create {result.ID}'},
                            headers=headers)
    except Exception as e:
        print(f"여기인가 ? {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create Users")
