import math

def paint_liters(net_m2: float, coverage_m2_per_l: float, coats: int) -> dict:
    if coverage_m2_per_l <= 0 or coats <= 0:
        raise ValueError("coverage and coats must be positive")
    need = float(net_m2) * int(coats) / float(coverage_m2_per_l)
    return {"liters": round(need, 2), "coats": int(coats), "coverage": float(coverage_m2_per_l)}

def paint_liters_tiered(net_m2: float, coverage_list: list[float]) -> dict:
    rates = [float(c) for c in coverage_list]
    if not rates or any(not math.isfinite(c) or c <= 0 for c in rates):
        raise ValueError("each coat coverage must be a positive number")
    need = sum(float(net_m2) / c for c in rates)
    return {"liters": round(need, 2), "coats": len(rates), "coverage_list": rates}
