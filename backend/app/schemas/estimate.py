from pydantic import BaseModel
class EstimateRequest(BaseModel):
    room_id: int
    coats: int | None = None
    coverage: float | None = None
    coverage_list: list[float] | None = None
    persist: bool = True
