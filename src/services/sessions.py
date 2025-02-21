from repositories.sessions import insert_session

def create_session(campaign_id: int, session_date: str, duration: int, notes: str) -> int:
    session_data = {
        "campaign_id": campaign_id,
        "session_date": session_date,
        "duration": duration,
        "notes": notes
    }
    try:
        return insert_session(session_data)
    except Exception as e:
        print("Ошибка создания сессии:", e)
        return -1
