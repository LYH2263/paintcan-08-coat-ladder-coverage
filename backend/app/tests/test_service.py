import json
import pytest
import app.db as db
from app import seed
from app.services.paint_service import PaintService

@pytest.fixture
def service(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    seed.init_db()
    with PaintService() as s:
        yield s

def _count(s):
    return s._c.execute("SELECT COUNT(*) c FROM calc_runs").fetchone()["c"]

def test_default_estimate_matches_base(service):
    # 与改造前同房同参结果一致：净46.41，8 m²/L × 2 遍 = 11.6 升
    r = service.estimate(1, False)
    assert r["run_id"] is None
    assert r["liters"] == 11.6
    assert r["coats"] == 2
    assert r["coverage"] == 8.0
    assert "coverage_ladder" not in r

def test_persist_false_writes_nothing(service):
    before = _count(service)
    r = service.estimate(1, False, coverage_ladder=[10, 8])
    assert r["run_id"] is None
    assert r["liters"] == 10.44
    assert _count(service) == before

def test_persist_true_pins_ladder(service):
    r = service.estimate(1, True, coverage_ladder=[10, 8])
    rid = r["run_id"]
    assert rid is not None
    row = service.history_one(rid)
    assert row["input"]["coverage_ladder"] == [10.0, 8.0]
    assert row["result"]["coverage_ladder"] == [10.0, 8.0]
    assert row["result"]["coat_liters"] == [4.64, 5.8]
    assert row["result"]["liters"] == 10.44

def test_invalid_ladder_rejected_without_row(service):
    before = _count(service)
    with pytest.raises(ValueError):
        service.estimate(1, True, coats=2, coverage_ladder=[10])   # 长度≠遍数
    with pytest.raises(ValueError):
        service.estimate(1, True, coverage_ladder=[10, 0])       # 非正
    with pytest.raises(ValueError):
        service.estimate(1, True, coats=3, coverage_ladder=[10, 8])
    assert _count(service) == before

def test_template_change_does_not_move_old_run(service):
    r = service.estimate(1, True, coverage_ladder=[10, 8])
    rid = r["run_id"]
    service.save_ladder_template([12, 9, 7])
    old = service.history_one(rid)
    assert old["result"]["liters"] == 10.44
    assert old["result"]["coverage_ladder"] == [10.0, 8.0]
    assert service.settings()["coverage_ladder_template"] == [12.0, 9.0, 7.0]

def test_ladder_implies_coats_when_omitted(service):
    r = service.estimate(1, False, coverage_ladder=[10, 8, 6])
    assert r["coats"] == 3
    assert len(r["coat_liters"]) == 3

def test_bad_template_rejected(service):
    with pytest.raises(ValueError):
        service.save_ladder_template([])
    with pytest.raises(ValueError):
        service.save_ladder_template([8, 0])
