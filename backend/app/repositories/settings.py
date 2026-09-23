import sqlite3
def get_map(conn): return {r["key"]: r["value"] for r in conn.execute("SELECT * FROM settings").fetchall()}
def set_map(conn, kv):
    for k, v in kv.items():
        conn.execute("INSERT INTO settings(key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (k, str(v)))
    conn.commit()
    return get_map(conn)
def coverage_coats(conn):
    m = get_map(conn)
    return float(m.get("coverage", "8")), int(m.get("coats", "2"))
