import streamlit as st
import pandas as pd
from datetime import timedelta
# Налаштування сторінки в діловому стилі
st.set_page_config(page_title="Travel Calc Pro", page_icon="✈️", layout="centered")
# Кастомний CSS для "мультяшного ділового" вигляду
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #004aad;
        color: white;
        border: 2px solid #003366;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #00d4ff;
        color: black;
        transform: scale(1.02);
    }
    .stDateInput, .stRadio, .stSelectbox {
        background-color: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.05);
    }
    h1, h2, h3 {
        color: #004aad;
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)
# --- Ініціалізація стану ---
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'data' not in st.session_state:
    st.session_state.data = {}
def go_to(page):
    st.session_state.page = page
    st.rerun()
# --- СТОРІНКА 1 ---
if st.session_state.page == 1:
    st.title("📂 Крок 1: Планування")
    st.write("---")
    st.markdown("### 🗓️ Термін основного заходу")
    st.caption("Вкажіть дати згідно із запрошенням")
    col1, col2 = st.columns(2)
    start_main = col1.date_input("Початок заходу", key="main_s")
    end_main = col2.date_input("Кінець заходу", key="main_e")
    main_days = (end_main - start_main).days + 1
    st.success(f"📈 Тривалість заходу: **{main_days}** дн.")
    st.write("---")
    st.markdown("### 🌍 Загальний термін відрядження")
    st.caption("Разом із днями в дорозі")
    col3, col4 = st.columns(2)
    start_total = col3.date_input("Дата початку", key="total_s")
    end_total = col4.date_input("Дата кінця", key="total_e")
    total_days = (end_total - start_total).days + 1
    st.info(f"⏳ Загальна тривалість: **{total_days}** дн.")
    st.write("")
    if st.button("Далі до дат переміщення ➡️"):
        st.session_state.data['start_total'] = start_total
        st.session_state.data['end_total'] = end_total
        go_to(2)
# --- СТОРІНКА 2 ---
elif st.session_state.page == 2:
    st.title("🚀 Крок 2: Логістика")
    st.write("---")
    with st.container():
        st.markdown("#### 🏢 Виїзд")
        d3 = st.date_input("📍 Дата виїзду з місця роботи")
        st.markdown("#### 🇬🇧 Прибуття")
        d4 = st.date_input("🛬 Дата прибуття в країну відрядження")
        st.markdown("#### 🛫 Вибуття")
        d5 = st.date_input("🛫 Дата вибуття з країни відрядження")
        st.markdown("#### 🏠 Повернення")
        d6 = st.date_input("🏁 Дата повернення в Україну")
    st.write("---")
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("⬅️ Назад до дат"): go_to(1)
    with col_next:
        if st.button("Далі до маршруту ➡️"):
            st.session_state.data.update({'d3': d3, 'd4': d4, 'd5': d5, 'd6': d6})
            go_to(3)
# --- СТОРІНКА 3 ---
elif st.session_state.page == 3:
    st.title("🛣️ Крок 3: Вибір маршруту")
    st.write("---")
    st.markdown("#### 🗺️ Як ви дістаєтесь до країни призначення?")
    route = st.radio("Оберіть свій варіант:", [
        "а. Прямий рейс (без ночівель та пересадок)",
        "б. Складний маршрут (пересадки/ночівлі)"
    ], help="Транзитні країни без зупинок не рахуються")
    st.write("---")
    col_prev, col_next = st.columns(2)
    with col_prev:
        if st.button("⬅️ Назад до логістики"): go_to(2)
    with col_next:
        if st.button("Далі до кордону ➡️"):
            st.session_state.data['route'] = route
            if "а." in route:
                go_to(4)
            else:
                st.warning("🧩 Цей модуль у розробці. Оберіть пункт 'а' для розрахунку.")
# --- СТОРІНКА 4 ---
elif st.session_state.page == 4:
    st.title("🛂 Крок 4: Деталі кордону")
    st.write("---")
    data = st.session_state.data
    q8_answer = None
    if data['d4'] != data['d3']:
        st.markdown("#### 🕒 Перетин кордону НА ПОЧАТКУ")
        q8_answer = st.radio("Коли ви перетнули український кордон?", 
                            ["а. першого дня до 23:59", "б. другого дня після 00:00"], 
                            index=0, key="q8")
    st.write("")
    q9_answer = None
    if data['d6'] != data['d5']:
        st.markdown("#### 🕒 Перетин кордону ПРИ ПОВЕРНЕННІ")
        q9_answer = st.radio("Коли ви в'їхали в Україну?", 
                            ["а. до 23:59 передостаннього дня", "б. після 00:00 останнього дня"], 
                            index=0, key="q9")
    st.write("---")
    if st.button("✨ СФОРМУВАТИ ТАБЛИЦЮ ✨"):
        all_dates = []
        current_date = data['start_total']
        while current_date <= data['end_total']:
            all_dates.append(current_date)
            current_date += timedelta(days=1)
        results = {}
        for dt in all_dates:
            results[dt] = "Велика Британія"
            if q8_answer == "б. другого дня після 00:00" and dt == data['d3']:
                results[dt] = "Україна"
            if q9_answer == "а. до 23:59 передостаннього дня" and dt == data['d6']:
                results[dt] = "Україна"

        st.session_state.final_df = pd.DataFrame({
            "Дата": results.keys(),
            "Добові по країні": results.values()
        })
        go_to(100)
# --- ФІНАЛЬНА СТОРІНКА ---
elif st.session_state.page == 100:
    st.title("📊 Ваш фінальний результат")
    st.balloons()
    st.markdown("#### Таблиця 1: Розрахунок добових")
    # Стилізація таблиці
    st.dataframe(st.session_state.final_df.style.set_properties(**{
        'background-color': '#f9f9f9',
        'color': '#004aad',
        'border-color': '#004aad'
    }), use_container_width=True)
    st.write("---")
    if st.button("🔄 Почати заново"):
        st.session_state.clear()
        go_to(1)
