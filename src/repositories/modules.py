import psycopg2
from psycopg2.extras import RealDictCursor

from settings import DB_CONFIG

def insert_module(module_data: dict) -> int:
    query = """
    INSERT INTO Modules (module_name, system_name, description, group_size)
    VALUES (%(module_name)s, %(system_name)s, %(description)s, %(group_size)s)
    RETURNING module_id;
    """
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, module_data)
            module_id = cur.fetchone()[0]
            conn.commit()
            return module_id

def list_modules() -> list[dict]:
    query = "SELECT * FROM Modules;"
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()
