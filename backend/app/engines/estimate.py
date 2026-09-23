from app.engines.paint_volume import paint_liters, paint_liters_ladder
from app.engines.wall_area import wall_area

def estimate_room(length, width, height, openings, coverage, coats, coverage_ladder=None):
    area = wall_area(length, width, height, openings)
    if coverage_ladder is not None:
        if len(coverage_ladder) != int(coats):
            raise ValueError("coverage_ladder length must equal coats")
        vol = paint_liters_ladder(area["net_m2"], coverage_ladder)
    else:
        vol = paint_liters(area["net_m2"], coverage, coats)
    return {**area, **vol}
