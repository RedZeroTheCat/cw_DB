import streamlit as st
from services.modules import create_module
from repositories.modules import list_modules


def show_common_info(user_role: str):
    st.title("Общая информация")
    st.write("Полезные тексты, советы и информация о модулях.")
    st.markdown("---")
    st.write("*Когда создаёте персонажа и не до конца понимаете как его прописать, ответьте на следующие вопросы:*\n\n"
             "Почему персонаж решил стать авантюристом? Какое событие его к этому подтолкнуло?\n\n"
             "Ради какой цели персонаж стал авантюристом?\n\n"
             "Какие гуманоиды или разумные существа знают персонажа? Кто является его другом, семьёй?")
    st.markdown("---")

    modules = list_modules()
    st.header("Модули")
    st.markdown("---")
    if modules:
        for module in modules:
            st.write(f"**{module['module_name']}** \n\n ({module['system_name']}): {module['description']} \n\n Рекомендуемый размер группы: {module['group_size']}")
            st.markdown("---")
    else:
        st.write("Модули не найдены.")

    if user_role == "master":
        st.header("Добавить новый модуль")
        module_name = st.text_input("Название модуля")
        system_name = st.text_input("Название системы")
        description = st.text_area("Описание")
        group_size = st.number_input("Рекомендуемый размер группы", min_value=1, step=1)
        if st.button("Добавить модуль"):
            module_id = create_module(module_name, system_name, description, group_size)
            if module_id != -1:
                st.success("Модуль успешно добавлен!")
            else:
                st.error("Ошибка добавления модуля.")