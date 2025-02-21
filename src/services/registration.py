import bcrypt
import datetime
from repositories.registration import insert_user

def register_user(fullname: str, social_media_link: str, age: int, role: str, password: str) -> bool:
    try:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_data = {
            "fullname": fullname,
            "social_media_link": social_media_link,
            "age": age,
            "role": role,
            "playing_since": datetime.date.today(),
            "password_hash": hashed.decode('utf-8')
        }
        insert_user(user_data)

        return True
    except Exception as e:
       print("Ошибка регистрации:", e)
       return False
