import streamlit as st

from repositories.users import get_user_dashboard
from repositories.sessions import get_next_session_date
from services.character_sheets import create_character_sheet

def show_player_dashboard(user_id: int):
    st.title("Панель Игрока")
    st.markdown("---")

    dashboard = get_user_dashboard(user_id)

    st.header("Ваши персонажи")
    if dashboard.get("characters"):
        for character in dashboard["characters"]:
            st.markdown("---")
            st.write(f"**{character['character_name']}**")
            st.write(f"{character.get('attributes')}")
            st.markdown("---")
            st.write(f"{character.get('background')}")
    else:
        st.write("Вы ещё не создали ни одного персонажа")

    st.markdown("---")
    st.subheader("Создать нового персонажа")
    character_name = st.text_input("Имя персонажа")
    attributes = st.text_area("Атрибуты (пример: Сила: 12, Ловкость: 14, Интеллект: 16)")
    background = st.text_area("Предыстория персонажа")

    if st.button("Создать персонажа"):
        if character_name and attributes and background:
            success = create_character_sheet(user_id, character_name, attributes, background)
            if success:
                st.success("Персонаж успешно создан!")
                st.rerun()
            else:
                st.error("Ошибка при создании персонажа")
        else:
            st.error("Заполните все поля!")

    st.header("Ваши достижения")
    if dashboard.get("achievements"):
        for ach in dashboard["achievements"]:
            st.write(f"{ach['name']}: {ach['description']} (Дата: {ach['date_awarded']})")
    else:
        st.write("Вам ещё не выдали ни одного достижения")

    st.header("Ваши группы")
    st.markdown("---")
    if dashboard.get("groups"):
        for group in dashboard["groups"]:
            role = "Мастер" if group["master_id"] == user_id else "Игрок"
            st.subheader(f"*{group['group_name']}* — {role}")

            if group.get("campaigns"):
                st.write("***Кампании группы:***")
                for campaign in group["campaigns"]:
                    next_session = get_next_session_date(campaign["campaign_id"])
                    if campaign["status"] == "active":
                        st.write(f"Кампания: **{campaign['name']}**. \n\nСледующая сессия: {next_session}")
                    else:
                        st.write(f"Кампания: **{campaign['name']}** (Статус: {campaign['status']})")
                    st.markdown("---")
    else:
        st.write("Вы не состоите ни в одной группе")
