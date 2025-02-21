import psycopg2
from psycopg2.extras import RealDictCursor
from settings import DB_CONFIG

def insert_character_sheet(character_data: dict) -> None:
    query = """
    INSERT INTO CharacterSheets (user_id, character_name, attributes, background)
    VALUES (%(user_id)s, %(character_name)s, %(attributes)s, %(background)s);
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, character_data)
            conn.commit()

def delete_character_sheet(character_id: int) -> None:
    query = "DELETE FROM CharacterSheets WHERE character_id = %s;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (character_id,))
            conn.commit()