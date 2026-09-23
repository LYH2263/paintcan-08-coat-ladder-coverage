from app.engines.paint_volume import paint_liters, paint_liters_tiered
from app.engines.wall_area import wall_area

def estimate_room(length, width, height, openings, coverage, coats, coverage_list=None):
    area = wall_area(length, width, height, openings)
    if coverage_list is not None:
        if len(coverage_list) != int(coats):
            raise ValueError("coverage_list length must equal coats")
        vol = paint_liters_tiered(area["net_m2"], coverage_list)
    else:
        vol = paint_liters(area["net_m2"], coverage, coats)
    return {**area, **vol}
