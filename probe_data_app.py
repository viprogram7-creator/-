import streamlit as st
import pandas as pd
from datetime import timedelta, date
# Налаштування сторінки
st.set_page_config(layout="wide", page_title="ДСНС - Кошторис")
# Спеціальні CSS-стилі для "мультяшної" ночі та кнопок
st.markdown("""
    <style>
    /* Стиль для контейнера з датами */
    .date-row {
        display: flex;
        align-items: center;
        gap: 10px;
        overflow-x: auto;
        padding: 20px;
    }
    /* Загальний стиль для кнопок ночівлі */
    div.stButton > button {
        width: 180px !important;
        height: 50px !important;
        border-radius: 12px;
        font-size: 16px !important;
        transition: 0.3s;
    }
    /* Синій фон: зорі та півмісяць */
    div.stButton > button.night-blue {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%) !important;
        color: #f1f5f9 !important;
        border: 1px solid #3b82f6 !important;
    }
    /* Зелений фон при натисканні */
    div.stButton > button.night-green {
        background: linear-gradient(135deg, #166534 0%, #22c55e 100%) !important;
        color: white !important;
        border: 2px solid #bef264 !important;
        box-shadow: 0 0 15px rgba(34, 197, 94, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)
st.title("💼 Розрахунок витрат на проживання")
# 1. Налаштування періоду
start_total = date(2026, 2, 1)
end_total = date(2026, 2, 9)
# Ночівлі за логікою відбуваються МІЖ днями (наприклад, з 2 на 3, з 3 на 4...)
night_starts = [date(2026, 2, i) for i in range(2, 8)]
# Створення списку дат
all_dates = []
curr = start_total
while curr <= end_total:
    all_dates.append(curr)
    curr += timedelta(days=1)
# Стан для збереження "зелених" натискань
if 'green_nights' not in st.session_state:
    st.session_state.green_nights = {d: False for d in night_starts}
# 2. Візуалізація рядочка
st.subheader("Загальний термін відрядження та ночівлі")
# Використовуємо велику кількість колонок для горизонтального ряду
cols = st.columns(len(all_dates) + len(night_starts))
col_ptr = 0
for i, dt in enumerate(all_dates):
    # Відображаємо дату
    cols[col_ptr].metric(label="Дата", value=dt.strftime("%d.%m"))
    col_ptr += 1
    # Якщо між цією датою та наступною є ночівля
    if dt in night_starts:
        with cols[col_ptr]:
            is_green = st.session_state.green_nights[dt]
            btn_label = "🌙✨ ночівля"
            btn_type = "night-green" if is_green else "night-blue" 
            # Використання контейнера для індивідуального стилю (Markdown hack)
            st.markdown(f'<div class="{btn_type}">', unsafe_allow_html=True)
            if st.button(btn_label, key=f"btn_{dt}"):
                st.session_state.green_nights[dt] = not is_green
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        col_ptr += 1
# 3. Виведення повідомлення
active_nights = [d for d, status in st.session_state.green_nights.items() if status]
if active_nights:
    st.info("💡 Витрати на найм житлового приміщення покриває ДСНС (для обраних ночівель)")
# 4. Формування Таблиці 1
st.write("---")
st.subheader("Таблиця 1")
table_rows = []
for dt in all_dates:
    # Перевіряємо, чи була ночівля, що призвела до витрат у цю дату
    # Зазвичай витрати за ніч рахуються на дату початку ночівлі або дату чекауту.
    # Тут ставимо "120 доларів", якщо відповідна ніч стала "зеленою".
    cost = "-"
    if dt in st.session_state.green_nights and st.session_state.green_nights[dt]:
        cost = "120 доларів"    
    table_rows.append({
        "Дата": dt.strftime("%d.%m.%Y"),
        "Країна": "Польща",
        "Витрати ДСНС": cost
    })
df = pd.DataFrame(table_rows)
st.table(df)
