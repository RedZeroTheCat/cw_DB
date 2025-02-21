import streamlit as st
from repositories.groups import get_all_groups
from services.groups import join_group, leave_group, create_new_group
from repositories.users import get_user_dashboard

def show_group_info(user_id: int, user_role: str):
    st.title("Список групп")

    groups = get_all_groups()
    user_dashboard = get_user_dashboard(user_id)
    user_groups = {group["group_id"]: group for group in user_dashboard.get("groups", [])}

    if groups:
        for group in groups:
            st.markdown("---")
            st.write(f"**{group['group_name']}** (Тип: {group['type']})")

            if group["group_id"] in user_groups:
                if group["master_id"] == user_id:
                    st.write("***Мастер***")
                else:
                    if st.button("Покинуть группу", key=f"leave_{group['group_id']}"):
                        if leave_group(user_id, group["group_id"]):
                            st.success("Вы покинули группу!")
                            st.rerun()
                        else:
                            st.error("Ошибка при выходе из группы.")
            else:
                if st.button("Вступить в группу", key=f"join_{group['group_id']}"):
                    if join_group(user_id, group["group_id"]):
                        st.success("Вы успешно вступили в группу!")
                        st.rerun()
                    else:
                        st.error("Ошибка при вступлении в группу.")
    else:
        st.write("Группы не найдены.")

    st.markdown("---")
    if user_role == "master":
        st.header("Создать новую группу")
        group_name = st.text_input("Название группы")
        session_type = st.selectbox("Тип сессии", ("online", "offline", "various"))
        if st.button("Создать группу"):
            group_id = create_new_group(user_id, group_name, session_type)
            if group_id != -1:
                st.success(f"Группа '{group_name}' создана!")
                st.rerun()
            else:
                st.error("Ошибка создания группы.")
