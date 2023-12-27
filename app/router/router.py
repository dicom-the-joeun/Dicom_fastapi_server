from fastapi import APIRouter

from app.controller import paitent_ctrl


router = APIRouter()

router.include_router(
    paitent_ctrl.router,
    prefix="/paitent",
    tags=["paitent"]
)
