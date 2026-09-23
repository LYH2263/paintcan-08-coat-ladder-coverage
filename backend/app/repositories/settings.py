import json, sqlite3
def get_map(conn): return {r["key"]: r["value"] for r in conn.execute("SELECT * FROM settings").fetchall()}
def coverage_coats(conn):
    m = get_map(conn)
    return float(m.get("coverage", "8")), int(m.get("coats", "2"))
def ladder_template(conn):
    v = get_map(conn).get("coverage_ladder_template")
    if not v: return None
    try:
        t = json.loads(v)
        return [float(x) for x in t] if isinstance(t, list) and t else None
    except (ValueError, TypeError):
        return None
def put(conn, key, value):
    conn.execute("INSERT INTO settings(key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))
    conn.commit()
