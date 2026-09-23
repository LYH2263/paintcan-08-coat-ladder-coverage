import json, math
from fastapi import APIRouter, HTTPException
from app.services.paint_service import PaintService
router = APIRouter()
@router.get("/settings")
def settings():
    with PaintService() as s: return s.settings()
@router.post("/settings")
def save_settings(body: dict[str, str]):
    if "coverage_tiers" in body:
        try:
            tiers = [float(x) for x in json.loads(body["coverage_tiers"])]
        except (TypeError, ValueError):
            raise HTTPException(400, "coverage_tiers must be a JSON list of positive numbers")
        if not tiers or any(not math.isfinite(c) or c <= 0 for c in tiers):
            raise HTTPException(400, "coverage_tiers must be a JSON list of positive numbers")
        body["coverage_tiers"] = json.dumps(tiers)
    with PaintService() as s: return s.save_settings(body)
