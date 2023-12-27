from fastapi import APIRouter

from app.controller import patient_ctrl


router = APIRouter()

router.include_router(
    patient_ctrl.router,
    prefix="/paitent",
    tags=["paitent"]
)
