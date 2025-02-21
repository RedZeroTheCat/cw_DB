import datetime
from repositories.achievements import insert_achievement

def award_achievement(name: str, description: str, campaign_id: int, user_id: int) -> int:
    achievement_data = {
        "name": name,
        "description": description,
        "campaign_id": campaign_id,
        "user_id": user_id,
        "date_awarded": datetime.date.today()
    }
    try:
        return insert_achievement(achievement_data)
    except Exception as e:
        print("Ошибка выдачи достижения:", e)
        return -1
