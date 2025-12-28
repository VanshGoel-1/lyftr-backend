from datetime import datetime
from app.models import get_connection

def insert_message(msg):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
        INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?)
        """, (
            msg["message_id"],
            msg["from"],
            msg["to"],
            msg["ts"],
            msg.get("text"),
            datetime.utcnow().isoformat() + "Z"
        ))
        conn.commit()
        return "created"
    except Exception:
        return "duplicate"
    finally:
        conn.close()

def list_messages(filters, limit, offset):
    conn = get_connection()
    cur = conn.cursor()

    where = []
    params = []

    if filters.get("from"):
        where.append("from_msisdn = ?")
        params.append(filters["from"])
    if filters.get("since"):
        where.append("ts >= ?")
        params.append(filters["since"])
    if filters.get("q"):
        where.append("LOWER(text) LIKE ?")
        params.append(f"%{filters['q'].lower()}%")

    where_sql = f"WHERE {' AND '.join(where)}" if where else ""

    cur.execute(f"""
    SELECT COUNT(*) FROM messages {where_sql}
    """, params)
    total = cur.fetchone()[0]

    cur.execute(f"""
    SELECT message_id, from_msisdn, to_msisdn, ts, text
    FROM messages
    {where_sql}
    ORDER BY ts ASC, message_id ASC
    LIMIT ? OFFSET ?
    """, params + [limit, offset])

    rows = cur.fetchall()
    conn.close()

    return total, rows

def get_stats():
    conn = get_connection()
    cur = conn.cursor()

    # total messages
    cur.execute("SELECT COUNT(*) FROM messages")
    total_messages = cur.fetchone()[0]

    # distinct senders count
    cur.execute("SELECT COUNT(DISTINCT from_msisdn) FROM messages")
    senders_count = cur.fetchone()[0]

    # messages per sender (top 10)
    cur.execute("""
        SELECT from_msisdn, COUNT(*) as cnt
        FROM messages
        GROUP BY from_msisdn
        ORDER BY cnt DESC
        LIMIT 10
    """)
    messages_per_sender = [
        {"from": row[0], "count": row[1]}
        for row in cur.fetchall()
    ]

    # first and last timestamps
    cur.execute("SELECT MIN(ts), MAX(ts) FROM messages")
    row = cur.fetchone()
    first_message_ts = row[0]
    last_message_ts = row[1]

    conn.close()

    return {
        "total_messages": total_messages,
        "senders_count": senders_count,
        "messages_per_sender": messages_per_sender,
        "first_message_ts": first_message_ts,
        "last_message_ts": last_message_ts,
    }
