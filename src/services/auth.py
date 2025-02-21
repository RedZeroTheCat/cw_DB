import bcrypt
from repositories.users import get_users_with_password

def authorize(link: str, password: str) -> bool:
    users = get_users_with_password()
    for user in users:
        if user["social_media_link"] == link:
            stored_hash = user["password_hash"]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                return True
    return False