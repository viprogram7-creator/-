import streamlit as st
from datetime import datetime
# --- Ініціалізація стану сторінок ---
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'countries' not in st.session_state:
    st.session_state.countries = [""]
# Функція для переходу на сторінку
def go_to(page_number):
    st.session_state.page = page_number
    st.rerun()
# --- Дані з Постанови №98 (Приклад списку) ---
POSTANOVA_COUNTRIES = [
    "Австрія", "Бельгія", "Велика Британія", "Греція", "Данія", "Естонія", 
    "Ізраїль", "Ірландія", "Іспанія", "Італія", "Канада", "Латвія", 
    "Литва", "Німеччина", "Норвегія", "Польща", "Словаччина", "США", 
    "Туреччина", "Угорщина", "Франція", "Чехія", "Швейцарія", "Швеція"]
# --- СТОРІНКА 1 ---
if st.session_state.page == 1:
    st.title("Сторінка 1")
    st.subheader("Оберіть напрям відрядження:")
    col1, col2 = st.columns(2)
    if col1.button("а. Україна"):
        st.toast("Ця функція ще недоступна", icon="⚠️")
    if col2.button("б. Закордон"):
        go_to(2)
# --- СТОРІНКА 2 ---
elif st.session_state.page == 2:
    st.title("Сторінка 2")
    st.subheader("Оберіть країну відрядження")
    st.info("Максимально можна обрати до 3 країн")
    selected_countries = []
    for i, country in enumerate(st.session_state.countries):
        selected = st.selectbox(f"Країна {i+1}", [""] + POSTANOVA_COUNTRIES, key=f"country_{i}")
        if selected:
            selected_countries.append(selected)
    # Кнопка додавання країни (+)
    if len(st.session_state.countries) < 3:
        if st.button("➕ Додати ще одну країну"):
            st.session_state.countries.append("")
            st.rerun()
    if len(selected_countries) > 0:
        if st.button("Далі ➡️"):
            go_to(3)
# --- СТОРІНКА 3 ---
elif st.session_state.page == 3:
    st.title("Сторінка 3")
    st.subheader("Оберіть тип відрядження")
    choice = st.radio("Тип:", ["а. Все що не має відношення до навчання: робочі зустрічі, польові навчання, конференції, забрати гуманітарку", "б. Навчання, тренінги"])
    if st.button("Далі ➡️"):
        go_to(4)
# --- СТОРІНКА 4 ---
elif st.session_state.page == 4:
    st.title("Сторінка 4")
    st.subheader("Хто фінансує відрядження?")
    finance = st.radio("Варіанти:", [
        "а. Всі витрати за рахунок приймаючої сторони",
        "б. За рахунок бюджету проєкту (кошти на рахунку установи)",
        "в. Всі витрати за рахунок ДСНС",
        "г. Частково приймаюча сторона / частково ДСНС"])
    if st.button("Далі ➡️"):
        if "а." in finance:
            go_to(5)
        elif "б." in finance or "в." in finance:
            go_to(7)
        elif "г." in finance:
            go_to(6)
# --- СТОРІНКА 5 ---
elif st.session_state.page == 5:
    st.title("Сторінка 5")
    st.success("При таких умовах складати кошторис не треба")
    if st.button("Повернутися на початок"):
        st.session_state.clear()
        st.rerun()
# --- СТОРІНКА 6 ---
elif st.session_state.page == 6:
    st.title("Сторінка 6")
    st.warning("""
    **Всі фінансові умови прописані в запрошені або додатку до нього (програма заходу).** Якщо усно обговорювалися питання фінансування, вони мають бути підкріплені додатковим офіційним документом.
    """)
    st.radio("1. Чи забезпечує приймаюча сторона добовими?", ["а. Так", "б. Ні"])
    st.radio("2. Чи забезпечує приймаюча сторона житлом?", [
        "а. Так (Будь-де під час всього відрядження)",
        "б. Частково (Тільки під час заходу на території країни)",
        "в. Частково (На шляху до країни та під час заходу)",
        "г. Ні"])
    st.radio("3. Чи забезпечує приймаюча сторона страхуванням?", ["а. Так", "б. Ні"])
    st.radio("4. Чи забезпечує приймаюча сторона харчуванням?", [
        "а. Так (Повністю)",
        "б. Частково",
        "в. Ні"])
    if st.button("Далі ➡️"):
        go_to(7)
# --- СТОРІНКА 7 ---
elif st.session_state.page == 7:
    st.title("Сторінка 7")
    st.subheader("Терміни відрядження")
    col1, col2 = st.columns(2)
    with col1:
        st.date_input("1. Термін основного заходу (З)", key="main_start")
        st.date_input("2. Загальний термін відрядження (З)", key="total_start")
    with col2:
        st.date_input("1. Термін основного заходу (ПО)", key="main_end")
        st.date_input("2. Загальний термін відрядження (ПО)", key="total_end")
    st.date_input("3. Вкажіть день виїзду з України", key="exit_ua")
    st.date_input("4. Вкажіть день повернення в Україну", key="return_ua")
    st.date_input("5. Вкажіть день прибуття в країну відрядження", key="arrival_dest")
    st.date_input("6. Вкажіть день виїзду з країни відрядження", key="exit_dest")
    if st.button("Сформувати результат"):
        st.balloons()
        st.success("Дані отримано! Можна переходити до розрахунку таблиці.")
