from fastapi import APIRouter, HTTPException
from app.schemas.estimate import LadderTemplateRequest
from app.services.paint_service import PaintService
router = APIRouter()
@router.get("/settings")
def settings():
    with PaintService() as s: return s.settings()
@router.post("/settings/ladder-template")
def save_ladder_template(body: LadderTemplateRequest):
    with PaintService() as s:
        try:
            return s.save_ladder_template(body.coverage_ladder)
        except ValueError as e:
            raise HTTPException(400, str(e))
