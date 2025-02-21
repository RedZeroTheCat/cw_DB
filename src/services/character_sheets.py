from repositories.character_sheets import insert_character_sheet, delete_character_sheet

def create_character_sheet(user_id: int, character_name: str, attributes: str, background: str) -> bool:
    character_data = {
        "user_id": user_id,
        "character_name": character_name,
        "attributes": attributes,
        "background": background
    }
    try:
        insert_character_sheet(character_data)
        return True
    except Exception as e:
        print("Ошибка создания листа персонажа:", e)
        return False

def remove_character_sheet(character_id: int) -> bool:
    try:
        delete_character_sheet(character_id)
        return True
    except Exception as e:
        print("Ошибка удаления листа персонажа:", e)
        return False