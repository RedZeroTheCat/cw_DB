from repositories.groups import create_group, add_user_to_group, remove_user_from_group

def create_new_group(creator_id: int, group_name: str, session_type: str) -> int:
    try:
        group_id = create_group(creator_id, group_name, session_type)
        add_user_to_group(group_id, creator_id)
        return group_id
    except Exception as e:
        print("Ошибка создания группы:", e)
        return -1

def join_group(user_id: int, group_id: int) -> bool:
    try:
        add_user_to_group(group_id, user_id)
        return True
    except Exception as e:
        print("Ошибка вступления в группу:", e)
        return False

def leave_group(user_id: int, group_id: int) -> bool:
    try:
        remove_user_from_group(group_id, user_id)
        return True
    except Exception as e:
        print("Ошибка выхода из группы:", e)
        return False