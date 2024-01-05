import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from starlette import status

from app.conf.db_config import DBConfig
from app.models.api_model import SelectThumbnail
from app.services.dcm_service import DcmService


router = APIRouter()
db = DBConfig()


@router.get("/image")
async def get_dcm_test(filepath: str, filename: str):
    image = DcmService.get_dcm_img(filepath, filename)
    if not image:
        raise HTTPException(status_code=404, detail="Patients not found")
    return StreamingResponse(image, media_type="image/png")


@router.get("/thumbnails", response_model=List[SelectThumbnail])
async def get_thumbnail(studykey: int, db: Session = Depends(db.get_db)):
    results = []
    thumbnails = await DcmService.get_dcm_thumbnails(studykey, db)
    if not thumbnails:
        raise HTTPException(status_code=404, detail = "Can't find thumbnail")
    for thumbnail in thumbnails:
        jsondata = DcmService.get_dcm_json(filepath=thumbnail.PATH,
                            filename=thumbnail.FNAME)
        json_dcm = json.loads(jsondata)
        if "Image Comments" in json_dcm:
            SCORE = json_dcm["Image Comments"]
        else:
            SCORE = None
        result = SelectThumbnail(
                    SERIESKEY=thumbnail.SERIESKEY,
                    SERIESDESC=thumbnail.SERIESDESC,
                    SCORE=SCORE,
                    PATH=thumbnail.PATH,
                    FNAME = thumbnail.FNAME
                ).dict()
        results.append(result)
    return JSONResponse(content=results, status_code=status.HTTP_200_OK)
