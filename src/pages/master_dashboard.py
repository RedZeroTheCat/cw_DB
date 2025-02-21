import streamlit as st
from repositories.users import get_user_dashboard
from repositories.groups import get_group_members
from repositories.modules import list_modules
from repositories.campaigns import update_campaign_status
from repositories.sessions import get_campaign_sessions
from services.campaigns import create_campaign
from services.sessions import create_session
from services.achievements import award_achievement

def show_master_dashboard(user_id: int):
    st.title("Панель Мастера")
    st.markdown("---")

    dashboard = get_user_dashboard(user_id)
    master_groups = [g for g in dashboard.get("groups", []) if g["master_id"] == user_id]

    st.header("Ваши группы и кампании")
    if master_groups:
        for group in master_groups:
            st.markdown("---")
            st.subheader(f"Группа: {group['group_name']}")

            st.write("Создать кампанию для этой группы")
            modules = list_modules()
            module_options = {m["module_id"]: f"{m['module_name']} ({m['system_name']})" for m in modules}
            selected_module_id = st.selectbox("Выберите модуль", list(module_options.keys()), format_func=lambda x: module_options[x], key=f"mod_{group['group_id']}")
            campaign_name = st.text_input("Название кампании", key=f"camp_name_{group['group_id']}")
            duration = st.number_input("Длительность (в сессиях)", min_value=1, step=1, key=f"camp_dur_{group['group_id']}")

            if st.button("Создать кампанию", key=f"create_camp_{group['group_id']}"):
                if campaign_name and selected_module_id:
                    campaign_data = {
                        "group_id": group["group_id"],
                        "module_id": selected_module_id,
                        "duration": duration,
                        "status": "active",
                        "name": campaign_name
                    }
                    campaign_id = create_campaign(campaign_data)
                    if campaign_id != -1:
                        st.success("Кампания успешно создана!")
                        st.rerun()
                    else:
                        st.error("Ошибка создания кампании")
                else:
                    st.error("Введите название кампании и выберите модуль!")

            if group.get("campaigns"):
                for campaign in group["campaigns"]:
                    st.markdown("---")
                    st.write(f"Кампания: **{campaign['name']}**")
                    st.write(f"Статус: {campaign['status']}")

                    new_status = st.selectbox("Изменить статус", ("active", "paused", "finished"),
                                              key=f"status_{campaign['campaign_id']}")
                    if st.button("Обновить статус", key=f"upd_status_{campaign['campaign_id']}"):
                        if update_campaign_status(campaign['campaign_id'], new_status):
                            st.success("Статус обновлён")
                        else:
                            st.error("Ошибка обновления статуса")

                    if campaign['status'] == "active":
                        st.markdown("---")
                        st.write("Создать новую сессию")
                        session_date = st.text_input("Дата сессии (YYYY-MM-DD)", key=f"sess_date_{campaign['campaign_id']}")
                        duration = st.number_input("Длительность сессии (в часах)", min_value=1,
                                                   key=f"sess_dur_{campaign['campaign_id']}")
                        notes = st.text_area("Заметки", key=f"sess_notes_{campaign['campaign_id']}")
                        if st.button("Создать сессию", key=f"create_sess_{campaign['campaign_id']}"):
                            if create_session(campaign['campaign_id'], session_date, duration, notes) != -1:
                                st.success("Сессия создана")
                            else:
                                st.error("Ошибка создания сессии")

                    st.markdown("---")
                    st.write("Все сессии кампании:")
                    sessions = get_campaign_sessions(campaign["campaign_id"])
                    if sessions:
                        for session in sessions:
                            st.write(f"{session['session_date']}: {session['notes']}")
                    else:
                        st.write("В этой кампании ещё не было сессий.")

                    st.markdown("---")
                    st.write("Выдать достижение")
                    group_members = get_group_members(group["group_id"])
                    player_options = {m["user_id"]: f"{m['fullname']} ({m['social_media_link']})" for m in group_members if m["user_id"] != user_id}
                    if player_options:
                        selected_user_id = st.selectbox("Выберите игрока", list(player_options.keys()), format_func=lambda x: player_options[x], key=f"player_{campaign['campaign_id']}")
                        ach_name = st.text_input("Название достижения", key=f"ach_name_{campaign['campaign_id']}")
                        ach_description = st.text_area("Описание достижения", key=f"ach_desc_{campaign['campaign_id']}")
                        if st.button("Выдать достижение", key=f"award_ach_{campaign['campaign_id']}"):
                            if award_achievement(ach_name, ach_description, campaign['campaign_id'], selected_user_id) != -1:
                                st.success("Достижение выдано!")
                            else:
                                st.error("Ошибка выдачи достижения.")
                    else:
                        st.write("Нет доступных игроков для выдачи достижения.")

    else:
        st.write("У вас нет групп, где вы выступаете в роли Мастера.")
