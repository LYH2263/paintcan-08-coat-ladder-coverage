from pydantic import BaseModel

class EstimateRequest(BaseModel):
    room_id: int
    coats: int | None = None
    coverage: float | None = None
    coverage_ladder: list[float] | None = None
    persist: bool = True

class LadderTemplateRequest(BaseModel):
    coverage_ladder: list[float]
