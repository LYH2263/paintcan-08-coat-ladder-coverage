import pytest
from app.engines.estimate import estimate_room
from app.engines.paint_volume import paint_liters, paint_liters_ladder
from app.engines.wall_area import wall_area

def test_living_room_net():
    a = wall_area(5, 4, 2.8, [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}])
    assert a["gross_m2"] == 50.4
    assert a["net_m2"] == 46.41

def test_liters_two_coats():
    v = paint_liters(46.41, 8, 2)
    assert v["liters"] == 11.6

def test_estimate_combined():
    e = estimate_room(5, 4, 2.8, [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}], 8, 2)
    assert e["liters"] == 11.6

def test_bad_coverage():
    with pytest.raises(ValueError):
        paint_liters(10, 0, 2)

def test_ladder_liters_sums_per_coat():
    v = paint_liters_ladder(46.41, [10, 8])
    assert v["coats"] == 2
    assert v["coverage_ladder"] == [10.0, 8.0]
    assert v["coat_liters"] == [4.64, 5.8]
    assert v["liters"] == 10.44

def test_ladder_nonpositive_rejected():
    with pytest.raises(ValueError):
        paint_liters_ladder(10, [8, 0])
    with pytest.raises(ValueError):
        paint_liters_ladder(10, [8, -1])

def test_ladder_empty_rejected():
    with pytest.raises(ValueError):
        paint_liters_ladder(10, [])

def test_estimate_ladder():
    e = estimate_room(5, 4, 2.8, [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}], 8, 2, [10, 8])
    assert e["liters"] == 10.44
    assert e["coat_liters"] == [4.64, 5.8]
    assert e["coverage_ladder"] == [10.0, 8.0]

def test_estimate_ladder_length_mismatch():
    with pytest.raises(ValueError):
        estimate_room(5, 4, 2.8, [], 8, 2, [10])
    with pytest.raises(ValueError):
        estimate_room(5, 4, 2.8, [], 8, 2, [10, 8, 6])

def test_default_path_unchanged():
    # 缺省仍为单一涂布率×遍数，且不含阶梯字段
    e = estimate_room(5, 4, 2.8, [{"w": 0.9, "h": 2.1}, {"w": 1.5, "h": 1.4}], 8, 2)
    assert e == {"gross_m2": 50.4, "openings_m2": 3.99, "net_m2": 46.41,
                 "liters": 11.6, "coats": 2, "coverage": 8.0}
