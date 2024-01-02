from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.conf.db_config import DBConfig
from app.models.api_model import SelectStudyViewTab
from app.services.study_service import StudyService


router = APIRouter()
db = DBConfig()


@router.get("/", response_model=List[SelectStudyViewTab])
async def get_patients(db : Session = Depends(db.get_db)):
    studies = StudyService.select_study_all(db)
    if not studies:
        raise HTTPException(status_code=404, detail="Patients not found")
    return studies