import psycopg2
from psycopg2.extras import RealDictCursor

from settings import DB_CONFIG

def create_group(creator_id: int, group_name: str, session_type: str) -> int:
    query = """
    INSERT INTO Groups (master_id, group_name, type) 
    VALUES (%s, %s, %s) RETURNING group_id;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (creator_id, group_name, session_type))
            group_id = cur.fetchone()[0]
            conn.commit()
            return group_id


def add_user_to_group(group_id: int, user_id: int) -> None:
    query = """
    INSERT INTO GroupMembers (group_id, user_id)
    VALUES (%s, %s);
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (group_id, user_id))
            conn.commit()

def remove_user_from_group(group_id: int, user_id: int) -> None:
    query = """
    DELETE FROM GroupMembers WHERE group_id = %s AND user_id = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (group_id, user_id))
            conn.commit()

def get_all_groups() -> list[dict]:
    query = "SELECT * FROM Groups;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()

def get_group_members(group_id: int) -> list[dict]:
    query = """
    SELECT u.user_id, u.fullname, u.social_media_link
    FROM GroupMembers gm
    JOIN Users u ON gm.user_id = u.user_id
    WHERE gm.group_id = %s;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (group_id,))
            return cur.fetchall()