import psycopg2
from psycopg2.extras import RealDictCursor

from settings import DB_CONFIG

def create_campaign(campaign_data: dict) -> int:
    query = """
    INSERT INTO Campaigns (group_id, module_id, duration, status, name)
    VALUES (%(group_id)s, %(module_id)s, %(duration)s, %(status)s, %(name)s)
    RETURNING campaign_id;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, campaign_data)
            campaign_id = cur.fetchone()[0]
            conn.commit()
            return campaign_id

def update_campaign_status(campaign_id: int, status: str) -> bool:
    query = "UPDATE Campaigns SET status = %s WHERE campaign_id = %s;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (status, campaign_id))
            conn.commit()
            return True

def get_campaigns_for_group(group_id: int) -> list[dict]:
    query = "SELECT campaign_id, name, status FROM Campaigns WHERE group_id = %s;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, group_id)
            return cur.fetchall()
