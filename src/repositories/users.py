import psycopg2
from psycopg2.extras import RealDictCursor

from settings import DB_CONFIG

def get_users() -> list[dict]:
    print("Receiving users")
    query = "SELECT user_id, fullname, social_media_link, role FROM users;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()

def get_users_with_password() -> list[dict]:
    print("Receiving users")
    query = "SELECT password_hash, social_media_link FROM users;"
    print(DB_CONFIG)
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()


def get_user_dashboard(user_id: int) -> dict:
    dashboard = {
        "characters": [],
        "achievements": [],
        "groups": []
    }

    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT character_name, attributes, background
                FROM CharacterSheets 
                WHERE user_id = %s;
            """, (user_id,))
            dashboard["characters"] = cur.fetchall()

            cur.execute("""
                SELECT name, description, date_awarded
                FROM Achievements 
                WHERE user_id = %s;
            """, (user_id,))
            dashboard["achievements"] = cur.fetchall()

            cur.execute("""
                SELECT g.group_id, g.group_name, g.master_id
                FROM Groups g
                JOIN GroupMembers gm ON g.group_id = gm.group_id
                WHERE gm.user_id = %s;
            """, (user_id,))
            groups = cur.fetchall()

            for group in groups:
                cur.execute("""
                    SELECT c.campaign_id, c.name, c.status, 
                            (SELECT MIN(session_date) 
                             FROM sessions s 
                             WHERE s.campaign_id = c.campaign_id) AS next_session
                    FROM Campaigns c WHERE c.group_id = %s;
                """, (group["group_id"],))
                group["campaigns"] = cur.fetchall()
            dashboard["groups"] = groups
    return dashboard

def get_user_data(social_media_link: str):
    query = "SELECT user_id, role FROM Users WHERE social_media_link = %s;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (social_media_link,))
            result = cur.fetchone()
            return result if result else (None, None)