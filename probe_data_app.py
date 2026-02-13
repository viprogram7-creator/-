import streamlit as st
import pandas as pd
from datetime import timedelta
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
    st.subheader("Терміни заходу та відрядження")
    # Питання 1
    st.write("Вкажіть дату проведення основного заходу (вказано в запрошенні):")
    col1, col2 = st.columns(2)
    start_main = col1.date_input("Початок заходу", key="main_s")
    end_main = col2.date_input("Кінець заходу", key="main_e")
    main_days = (end_main - start_main).days + 1
    st.info(f"Тривалість заходу: {main_days} дн.")
    # Питання 2
    st.write("Вкажіть загальний термін відрядження разом з дорогою:")
    col3, col4 = st.columns(2)
    start_total = col3.date_input("Дата початку", key="total_s")
    end_total = col4.date_input("Дата кінця", key="total_e")
    total_days = (end_total - start_total).days + 1
    st.info(f"Загальна тривалість: {total_days} дн.")
    if st.button("Далі ➡️"):
        st.session_state.data['start_total'] = start_total
        st.session_state.data['end_total'] = end_total
        go_to(2)
# --- СТОРІНКА 2 ---
elif st.session_state.page == 2:
    st.subheader("Дати переміщення")
    d3 = st.date_input("Вкажіть дату виїзду з місця роботи")
    d4 = st.date_input("Вкажіть дату прибуття в країну відрядження")
    d5 = st.date_input("Вкажіть дату вибуття з країни відрядження")
    d6 = st.date_input("Вкажіть дату повернення в Україну в місто роботи")
    col_prev, col_next = st.columns(2)
    if col_prev.button("⬅️ Назад"):
        go_to(1)
    if col_next.button("Далі ➡️"):
        st.session_state.data.update({'d3': d3, 'd4': d4, 'd5': d5, 'd6': d6})
        go_to(3)
# --- СТОРІНКА 3 ---
elif st.session_state.page == 3:
    st.subheader("Маршрут")
    st.write("Маршрут до країни відрядження відбувається:")
    route = st.radio("Оберіть варіант:", [
        "а. Прямий рейс без зупинок та ночівель",
        "б. На шляху є пересадки або зупинки на ночівлю"])
    col_prev, col_next = st.columns(2)
    if col_prev.button("⬅️ Назад"):
        go_to(2)
    if col_next.button("Далі ➡️"):
        st.session_state.data['route'] = route
        if "а." in route:
            go_to(4)
        else:
            st.warning("Сторінка для варіанту 'б' у розробці. Оберіть 'а' для тестування.")
# --- СТОРІНКА 4 ---
elif st.session_state.page == 4:
    st.subheader("Перетин кордону")
    data = st.session_state.data
    # Логіка Питання 8
    q8_answer = None
    if data['d4'] != data['d3']:
        st.write("Коли відбувається перетин українського кордону на початку поїздки?")
        q8_answer = st.radio("Вибір:", ["а. першого дня до 23:59", "б. другого дня після 00:00"], key="q8")
    # Логіка Питання 9
    q9_answer = None
    if data['d6'] != data['d5']:
        st.write("Коли відбувається перетин українського кордону при поверненні в Україну?")
        q9_answer = st.radio("Вибір:", ["а. до 23:59 передостаннього дня", "б. після 00:00 останнього дня"], key="q9")
    if st.button("Сформувати таблицю 📊"):
        # Генеруємо список усіх дат
        all_dates = []
        current_date = data['start_total']
        while current_date <= data['end_total']:
            all_dates.append(current_date)
            current_date += timedelta(days=1)
        results = {}
        target_country = "Велика Британія"
        for dt in all_dates:
            # За замовчуванням
            results[dt] = target_country
            # Обробка початку поїздки (Питання 8)
            if q8_answer == "б. другого дня після 00:00":
                if dt == data['d3']:
                    results[dt] = "Україна"
            # Обробка повернення (Питання 9)
            if q9_answer == "а. до 23:59 передостаннього дня":
                if dt == data['d6']:
                    results[dt] = "Україна"
            elif q9_answer == "б. після 00:00 останнього дня":
                # Всі дні залишаються Британією згідно вашої умови
                pass
        # Створення фінальної таблиці
        df = pd.DataFrame({
            "Дата": results.keys(),
            "Добові по країні": results.values()})
        st.session_state.final_df = df
        go_to(100) # Фінальна сторінка
# --- ФІНАЛЬНА СТОРІНКА ---
elif st.session_state.page == 100:
    st.subheader("Таблиця 1")
    st.table(st.session_state.final_df)
    if st.button("🔄 Почати заново"):
        st.session_state.clear()
        go_to(1)
