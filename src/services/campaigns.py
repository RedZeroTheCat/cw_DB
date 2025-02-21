from repositories.campaigns import create_campaign

def create_new_campaign(group_id: int, module_id: int, duration: int, next_session: str) -> int:
    campaign_data = {
        "group_id": group_id,
        "module_id": module_id,
        "duration": duration,
        "next_session": next_session  # передавать в формате 'YYYY-MM-DD'
    }
    try:
        return create_campaign(campaign_data)
    except Exception as e:
        print("Ошибка создания кампании:", e)
        return -1
