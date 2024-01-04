from fastapi import APIRouter

from app.controller import (patient_ctrl, auth_ctrl, study_ctrl, user_ctrl, dcm_ctrl)


router = APIRouter()

router.include_router(
    patient_ctrl.router,
    prefix="/paitents",
    tags=["paitents"]
)

router.include_router(
    auth_ctrl.router,
    prefix="/auth",
    tags=["auth"]
)

router.include_router(
    user_ctrl.router,
    prefix="/users",
    tags=["users"]
)

router.include_router(
    dcm_ctrl.router,
    prefix="/dcms",
    tags=["dcms"]
)

router.include_router(
    study_ctrl.router,
    prefix="/studies",
    tags=["studies"]
)
