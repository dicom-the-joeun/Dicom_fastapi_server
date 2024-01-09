import json
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from app.conf.config import security
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import HTTPAuthorizationCredentials
from app.conf.db_config import DBConfig
from app.models.api_model import SelectThumbnail
from app.services.dcm_service import DcmService
from app.services.user_service import UserService
from app.util.token_gen import verify_access_token


router = APIRouter()
db = DBConfig()


@router.get("/image")
async def get_dcm_image(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)], filepath: str, filename: str, db: Session = Depends(db.get_db)):
    id = verify_access_token(credentials.credentials)
    if not UserService.exisiting_user(id, db):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Cannot find user")
    image = DcmService.get_dcm_img(filepath, filename)
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patients not found")
    return StreamingResponse(image, media_type="image/png", status_code=status.HTTP_200_OK)


@router.get("/thumbnails", response_model=List[SelectThumbnail])
async def get_thumbnail(studykey: int, db: Session = Depends(db.get_db)):
    results = []
    thumbnails = await DcmService.get_seriestab_all_studykey(studykey, db)
    if not thumbnails:
        raise HTTPException(status_code=404, detail="Can't find thumbnail")
    for thumbnail in thumbnails:
        jsondata = DcmService.get_dcm_json(filepath=thumbnail.PATH,
                                           filename=thumbnail.FNAME)
        json_dcm = json.loads(jsondata)
        if "Image Comments" in json_dcm:
            SCORE = json_dcm["Image Comments"]
        else:
            SCORE = None
        result_by_one = SelectThumbnail(
            SERIESKEY=thumbnail.SERIESKEY,
            SERIESDESC=thumbnail.SERIESDESC,
            SCORE=SCORE,
            IMAGECNT=thumbnail.IMAGECNT,
            PATH=thumbnail.PATH,
            FNAME=thumbnail.FNAME,
            HEADERS= json.dumps(json_dcm)
        ).dict()
        results.append(result_by_one)
    return JSONResponse(content=results, status_code=status.HTTP_200_OK)


@router.get("/details", description="시리즈에서 이미지랑 모든 Header가져오기")
async def get_details(studykey: int, serieskey: int, db: Session = Depends(db.get_db)):
    result = await DcmService.get_seriestab_one(studykey=studykey, serieskey=serieskey, db=db)
    json_data = DcmService.get_dcm_json(filepath=result[0].PATH,
                                        filename=result[0].FNAME)
    result_json = json.loads(json_data)
    result = jsonable_encoder(result)
    result_json['result'] = result
    return JSONResponse(content=result_json, status_code=status.HTTP_200_OK)
