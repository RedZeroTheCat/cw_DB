import streamlit as st
from services.auth import authorize
from services.registration import register_user
from repositories.users import get_user_data
from pages.player_dashboard import show_player_dashboard
from pages.master_dashboard import show_master_dashboard
from pages.common_info import show_common_info
from pages.group_info import show_group_info

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "user_role" not in st.session_state:
    st.session_state["user_role"] = None


def login():
    st.title("Авторизация")
    st.write("Введите ссылку на соц.сеть и пароль:")

    social_media_link = st.text_input("Ссылка на соц.сеть")
    password = st.text_input("Пароль", type="password")

    if st.button("Войти"):
        if authorize(social_media_link, password):
            user_id, user_role = get_user_data(social_media_link)
            if user_id:
                st.session_state["authenticated"] = True
                st.session_state["user_id"] = user_id
                st.session_state["user_role"] = user_role
                st.success(f"Добро пожаловать!")
                st.rerun()
        else:
            st.error("Неверный логин или пароль!")


def register():
    st.title("Регистрация")
    st.write("Введите данные:")

    fullname = st.text_input("ФИО")
    social_media_link = st.text_input("Ссылка на соц.сеть")
    age = st.number_input("Возраст", min_value=10, max_value=100, step=1)
    role = "user"
    password = st.text_input("Пароль", type="password")
    password_confirm = st.text_input("Подтвердите пароль", type="password")

    if st.button("Зарегистрироваться"):
        if not fullname or not social_media_link or not password or not password_confirm:
            st.error("Заполните все поля!")
        elif password != password_confirm:
            st.error("Пароли не совпадают!")
        else:
            if register_user(fullname, social_media_link, age, role, password):
                st.success("Регистрация успешна! Теперь войдите в систему.")
            else:
                st.error("Ошибка регистрации. Возможно, такой пользователь уже существует.")


def main():
    if not st.session_state["authenticated"]:
        page = st.radio("Войдите или зарегистрируйтесь", ["Вход", "Регистрация"])
        if page == "Вход":
            login()
        elif page == "Регистрация":
            register()
    else:
        page = st.sidebar.radio(
            "Перейти к странице",
            ["Главная", "Панель игрока", "Группы"] if st.session_state["user_role"] == "user"
            else ["Главная", "Панель игрока", "Панель мастера", "Группы"]
        )

        if page == "Главная":
            show_common_info(st.session_state["user_role"])
        elif page == "Панель игрока":
            show_player_dashboard(st.session_state["user_id"])
        elif page == "Панель мастера" and st.session_state["user_role"] == "master":
            show_master_dashboard(st.session_state["user_id"])
        elif page == "Группы":
            show_group_info(st.session_state["user_id"], st.session_state["user_role"])


if __name__ == "__main__":
    main()
