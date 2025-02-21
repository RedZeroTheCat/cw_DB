import psycopg2
from psycopg2.extras import RealDictCursor
from settings import DB_CONFIG

def insert_session(session_data: dict) -> int:
    query = """
    INSERT INTO Sessions (campaign_id, session_date, duration, notes)
    VALUES (%(campaign_id)s, %(session_date)s, %(duration)s, %(notes)s)
    RETURNING session_id;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, session_data)
            session_id = cur.fetchone()[0]
            conn.commit()
            return session_id

def get_next_session_date(campaign_id: int) -> str:
    query = "SELECT MAX(session_date) AS next_session FROM Sessions WHERE campaign_id = %s;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (campaign_id,))
            result = cur.fetchone()
            return result[0] if result else None

def update_session_notes(session_id: int, notes: str) -> bool:
    query = "UPDATE Sessions SET notes = %s WHERE session_id = %s;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (notes, session_id))
            conn.commit()
            return True

def get_campaign_sessions(campaign_id: int) -> list[dict]:
    query = """
    SELECT session_date, notes 
    FROM Sessions 
    WHERE campaign_id = %s
    ORDER BY session_date ASC;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (campaign_id,))
            return cur.fetchall()