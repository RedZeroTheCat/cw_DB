import psycopg2
from psycopg2.extras import RealDictCursor

from settings import DB_CONFIG

def insert_user(user_data: dict) -> None:
    query = """
    INSERT INTO Users (fullname, social_media_link, age, role, playing_since, password_hash)
    VALUES (%(fullname)s, %(social_media_link)s, %(age)s, %(role)s, %(playing_since)s, %(password_hash)s);
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, user_data)
            conn.commit()