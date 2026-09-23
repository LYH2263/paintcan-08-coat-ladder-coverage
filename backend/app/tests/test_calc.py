import pytest
from app.engines.estimate import estimate_room
from app.engines.paint_volume import paint_liters, paint_liters_tiered
from app.engines.wall_area import wall_area

OPS = [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}]

def test_living_room_net():
    a = wall_area(5, 4, 2.8, OPS)
    assert a["gross_m2"] == 50.4
    assert a["net_m2"] == 46.41

def test_liters_two_coats():
    v = paint_liters(46.41, 8, 2)
    assert v["liters"] == 11.6

def test_estimate_combined():
    e = estimate_room(5, 4, 2.8, OPS, 8, 2)
    assert e["liters"] == 11.6

def test_bad_coverage():
    with pytest.raises(ValueError):
        paint_liters(10, 0, 2)

def test_tiered_uniform_matches_single():
    t = paint_liters_tiered(46.41, [8, 8])
    assert t["liters"] == paint_liters(46.41, 8, 2)["liters"] == 11.6
    assert t["coats"] == 2
    assert t["coverage_list"] == [8.0, 8.0]

def test_tiered_sums_each_coat():
    t = paint_liters_tiered(10, [5, 10, 20])
    assert t["liters"] == 3.5
    assert t["coats"] == 3

def test_tiered_rejects_nonpositive():
    for bad in ([8, 0], [8, -1], [], [8, float("nan")], [8, float("inf")]):
        with pytest.raises(ValueError):
            paint_liters_tiered(10, bad)

def test_estimate_tiered_length_mismatch():
    with pytest.raises(ValueError):
        estimate_room(5, 4, 2.8, OPS, 8, 2, [8, 8, 8])

def test_estimate_tiered_rejects_nonpositive():
    with pytest.raises(ValueError):
        estimate_room(5, 4, 2.8, OPS, 8, 2, [8, 0])

def test_estimate_tiered_parity_with_default():
    a = estimate_room(5, 4, 2.8, OPS, 8, 2)
    b = estimate_room(5, 4, 2.8, OPS, 8, 2, [8, 8])
    assert a["net_m2"] == b["net_m2"]
    assert a["liters"] == b["liters"]

def test_estimate_tiered_mixed_rates():
    e = estimate_room(5, 4, 2.8, OPS, 8, 3, [8, 10, 12])
    assert e["liters"] == round(46.41 / 8 + 46.41 / 10 + 46.41 / 12, 2)
    assert e["coats"] == 3
    assert e["coverage_list"] == [8.0, 10.0, 12.0]
