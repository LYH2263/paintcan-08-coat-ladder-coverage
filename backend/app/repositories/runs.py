import json, sqlite3
from datetime import datetime, timezone
def insert(conn, kind, payload, result, room_id=None):
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute("INSERT INTO calc_runs(kind,room_id,input_json,result_json,created_at) VALUES (?,?,?,?,?)",
        (kind, room_id, json.dumps(payload, ensure_ascii=False), json.dumps(result, ensure_ascii=False), now))
    conn.commit(); return int(cur.lastrowid)
def _row(r):
    d = dict(r)
    d["input"] = json.loads(d["input_json"]) if d.get("input_json") else None
    d["result"] = json.loads(d["result_json"]) if d.get("result_json") else None
    return d
def list_recent(conn, limit=50):
    return [_row(r) for r in conn.execute("SELECT * FROM calc_runs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()]
def get_by_id(conn, run_id):
    r = conn.execute("SELECT * FROM calc_runs WHERE id=?", (run_id,)).fetchone()
    return _row(r) if r else None
