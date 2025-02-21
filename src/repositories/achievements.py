import psycopg2

from settings import DB_CONFIG

def insert_achievement(achievement_data: dict) -> int:
    query = """
    INSERT INTO Achievements (name, description, campaign_id, user_id, date_awarded)
    VALUES (%(name)s, %(description)s, %(campaign_id)s, %(user_id)s, %(date_awarded)s)
    RETURNING achievement_id;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, achievement_data)
            achievement_id = cur.fetchone()[0]
            conn.commit()
            return achievement_id
