from typing import Annotated,List
from fastapi import APIRouter, Depends, HTTPException
from fastapi import security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.conf.DBConfig import DBConfig
from app.models.api_model import SelectPatient
from app.models.db_model import PatientTab
from app.services.patient_service import PatientService


router = APIRouter()
db = DBConfig()


@router.get("/", response_model=List[SelectPatient])
async def get_patients(id: str, db : Session = Depends(db.get_db)):
    patients = PatientService.select_record_all(id, db)
    if not patients:
        raise HTTPException(status_code=404, detail="Patients not found")
    return patients