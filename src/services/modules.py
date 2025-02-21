from repositories.modules import insert_module

def create_module(module_name: str, system_name: str, description: str, group_size: int) -> int:
    module_data = {
        "module_name": module_name,
        "system_name": system_name,
        "description": description,
        "group_size": group_size
    }
    try:
        return insert_module(module_data)
    except Exception as e:
        print("Ошибка создания модуля:", e)
        return -1
