from datetime import datetime
from app.models.api_model import SelectPatient
from app.models.db_model import PatientTab
import logging

from typing import List

class PatientService:
    @staticmethod
    def select_record_all(id, db) -> List[SelectPatient]:
        patients = db.query(PatientTab).filter(PatientTab.PID == id).all()
        return patients  # 이미 PatientTab 모델의 인스턴스 리스트이므로, 그대로 반환합니다.

    