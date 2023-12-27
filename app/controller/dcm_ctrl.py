from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from starlette import status

from app.conf.db_config import DBConfig
from app.models.api_model import SelectPatient
from app.services.dcm_service import DcmService


router = APIRouter()
db = DBConfig()


@router.get("/", response_model=List[SelectPatient])
async def get_dcm(filepath: str, filename: str):
    patients = DcmService.get_dcm(filepath, filename)
    print(patients)
    if not patients:
        raise HTTPException(status_code=404, detail="Patients not found")
    return JSONResponse(content=patients, status_code=status.HTTP_200_OK)