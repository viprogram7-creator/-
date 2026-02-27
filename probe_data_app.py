import streamlit as st
import pandas as pd
from datetime import timedelta, date
# Налаштування стилю для "мультяшної" ночівлі
st.markdown("""
    <style>
    /* Стиль для синьої кнопки (ніч) */
    div.stButton > button.night-btn {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        border-radius: 15px;
        border: 1px solid #ffffff;
        padding: 10px;
        font-size: 14px;
    }
    /* Стиль для зеленої кнопки (активовано) */
    div.stButton > button.active-btn {
        background-color: #22c55e !important;
        color: white !important;
        border: 2px solid #166534 !important;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("🌙 Планування проживання")
# 1. Визначення дат
start_date = date(2026, 2, 1)
end_date = date(2026, 2, 9)
night_range = [date(2026, 2, i) for i in range(2, 8)] # з 2 по 7
# Створюємо список усіх дат відрядження
all_dates = []
curr = start_date
while curr <= end_date:
    all_dates.append(curr)
    curr += timedelta(days=1)
# Ініціалізація стану для кліків по "ночівлі"
if 'active_nights' not in st.session_state:
    st.session_state.active_nights = {d: False for d in night_range}
# 2. Відображення дат у рядочок
st.subheader("Загальний термін відрядження")
cols = st.columns(len(all_dates) + len(night_range)) # Дати + слоти для ночівель
col_idx = 0
for i, dt in enumerate(all_dates):
    # Відображаємо дату
    cols[col_idx].write(dt.strftime("%d.%m"))
    col_idx += 1
    # Якщо після цієї дати йде ночівля (між датами)
    if dt in night_range:
        with cols[col_idx]:
            # Створюємо унікальний ключ для кнопки
            btn_key = f"night_{dt}"
            is_active = st.session_state.active_nights[dt]
            # Текст та стиль кнопки
            label = "🌙✨ ночівля"
            btn_class = "active-btn" if is_active else "night-btn"
            # Streamlit кнопки не підтримують CSS класи нативно через st.button, 
            # тому використовуємо маленький трюк з наданням стилю через контейнер або просто умову
            if st.button(label, key=btn_key):
                st.session_state.active_nights[dt] = not is_active
                st.rerun()
        col_idx += 1
# 3. Повідомлення
active_count = sum(st.session_state.active_nights.values())
if active_count > 0:
    st.success("✅ Витрати на найм житлового приміщення покриває ДСНС")
# 4. Формування Таблиці 1
st.write("---")
st.subheader("Таблиця 1")
table_data = []
for dt in all_dates:
    # Перевіряємо, чи була ночівля ПЕРЕД цією датою (чекін) 
    # або чи активна ночівля, що асоційована з цією датою
    is_covered = st.session_state.active_nights.get(dt, False)
    table_data.append({
        "Дата": dt.strftime("%d.%m.%Y"),
        "Польща": "Так",
        "Витрати (Зелені)": "120 доларів" if is_covered else "-"
    })
df = pd.DataFrame(table_data)
st.table(df)
if st.button("🔄 Скинути вибір"):
    st.session_state.active_nights = {d: False for d in night_range}
    st.rerun()
