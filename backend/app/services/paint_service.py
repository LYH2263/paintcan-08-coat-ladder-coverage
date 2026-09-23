import json
from app.db import connect
from app.engines.estimate import estimate_room
from app.repositories import openings, rooms, runs, settings as settings_repo

class PaintService:
    def __init__(self): self._c = connect()
    def close(self): self._c.close()
    def __enter__(self): return self
    def __exit__(self, *a): self.close()
    def list_rooms(self): return rooms.list_all(self._c)
    def room_detail(self, rid):
        r = rooms.get(self._c, rid)
        if not r: return None
        return {"room": r, "openings": openings.for_room(self._c, rid)}
    def settings(self):
        m = settings_repo.get_map(self._c)
        return {**m, "coverage_ladder_template": settings_repo.ladder_template(self._c)}
    def save_ladder_template(self, ladder):
        ladder = [float(x) for x in ladder]
        if not ladder or any(c <= 0 for c in ladder):
            raise ValueError("template must be a non-empty list of positive coverages")
        settings_repo.put(self._c, "coverage_ladder_template", json.dumps(ladder))
        return {"coverage_ladder_template": ladder}
    def history(self, limit=50): return runs.list_recent(self._c, limit)
    def history_one(self, run_id): return runs.get_by_id(self._c, run_id)
    def estimate(self, room_id, persist, coats=None, coverage=None, coverage_ladder=None):
        detail = self.room_detail(room_id)
        if not detail: return None
        r = detail["room"]
        cov, ct = settings_repo.coverage_coats(self._c)
        cov = float(coverage) if coverage is not None else cov
        if coverage_ladder is not None:
            ladder = [float(x) for x in coverage_ladder]
            ct = int(coats) if coats is not None else len(ladder)
            if len(ladder) != ct or any(c <= 0 for c in ladder):
                raise ValueError("coverage_ladder length must equal coats and every coverage be positive")
        else:
            ladder = None
            ct = int(coats) if coats is not None else ct
        ops = [{"w": o["w"], "h": o["h"]} for o in detail["openings"]]
        # 计算在写库之前：校验失败会抛出，整单拒绝且不写记录
        result = estimate_room(r["length"], r["width"], r["height"], ops, cov, ct, ladder)
        payload = {"room_id": room_id, "coats": ct}
        if ladder is not None:
            payload["coverage_ladder"] = ladder  # 钉选：逐遍涂布率随记录固化
        else:
            payload["coverage"] = cov
        rid = runs.insert(self._c, "estimate", payload, result, room_id) if persist else None
        return {"run_id": rid, "room_id": room_id, **result}
    def dashboard(self):
        rs = rooms.list_all(self._c)
        return {"room_count": len(rs), "clean": len([x for x in rs if "种子" not in x["name"] and "多种" not in x["name"]]), "dirty": len([x for x in rs if "多种" in x["name"]])}
