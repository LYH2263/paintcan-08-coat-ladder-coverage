def paint_liters(net_m2: float, coverage_m2_per_l: float, coats: int) -> dict:
    if coverage_m2_per_l <= 0 or coats <= 0:
        raise ValueError("coverage and coats must be positive")
    need = float(net_m2) * int(coats) / float(coverage_m2_per_l)
    return {"liters": round(need, 2), "coats": int(coats), "coverage": float(coverage_m2_per_l)}


def paint_liters_ladder(net_m2: float, coverage_ladder: list) -> dict:
    """逐遍涂布率：每一遍都按同一净面积除以该遍涂布率，再累加得升数。"""
    if not isinstance(coverage_ladder, (list, tuple)) or len(coverage_ladder) == 0:
        raise ValueError("coverage_ladder must be a non-empty list")
    try:
        ladder = [float(x) for x in coverage_ladder]
    except (TypeError, ValueError):
        raise ValueError("coverage_ladder entries must be numbers")
    if any(c <= 0 for c in ladder):
        raise ValueError("every coat coverage must be positive")
    coat_need = [float(net_m2) / c for c in ladder]
    return {
        "liters": round(sum(coat_need), 2),
        "coats": len(ladder),
        "coverage_ladder": ladder,
        "coat_liters": [round(x, 2) for x in coat_need],
    }
