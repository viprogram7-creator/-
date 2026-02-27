import streamlit as st
from datetime import timedelta, date
st.set_page_config(layout="wide", page_title="Схема ночівель ДСНС")
# --- СТИЛІЗАЦІЯ ---
st.markdown("""
    <style>
    /* Контейнер для схеми */
    .timeline-container {
        display: flex;
        align-items: center;
        justify-content: start;
        overflow-x: auto;
        padding: 40px 10px;
        background-color: #f8f9fa;
        border-radius: 15px;
    }
    /* Стиль дати (кілочок) */
    .date-point {
        text-align: center;
        min-width: 60px;
        font-weight: bold;
        color: #475569;
    }
    /* Загальний стиль для кнопок-ночей */
    div.stButton > button {
        height: 60px !important;
        margin-top: 10px;
        border-radius: 10px !important;
        border: none !important;
        transition: 0.3s !important;
        font-weight: bold !important;
    }
    /* Сіра ніч (не обрано) */
    div.stButton > button.night-off {
        background-color: #e2e8f0 !important;
        color: #64748b !important;
    }
    /* Зелена ніч (обрано) */
    div.stButton > button.night-on {
        background-color: #22c55e !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("🌙 Візуальна схема ночівель")
st.write("Натисніть на сірий блок ночівлі, щоб зробити його зеленим (оплата ДСНС).")
# 1. Дати (приклад)
start_dt = date(2026, 2, 1)
end_dt = date(2026, 2, 9)
# Створюємо список ночей
nights = []
curr = start_dt
while curr < end_dt:
    nights.append(curr)
    curr += timedelta(days=1)
# Ініціалізація стану
if 'active_nights' not in st.session_state:
    st.session_state.active_nights = {d: False for d in nights}
# 2. ПОБУДОВА СХЕМИ
# Створюємо багато колонок: по одній для дати, по одній для ночі
# Кількість колонок = дні + ночі
total_cols = len(nights) * 2 + 1
cols = st.columns(total_cols)
col_ptr = 0
for i, d in enumerate(nights):
    # Відображаємо дату (кілочок)
    with cols[col_ptr]:
        st.markdown(f"<div class='date-point'>{d.strftime('%d.%m')}</div>", unsafe_allow_html=True)
    col_ptr += 1
    # Відображаємо ніч (кнопка)
    with cols[col_ptr]:
        is_active = st.session_state.active_nights[d]
        label = "Ніч"
        # Використовуємо ключ для ідентифікації
        if st.button(label, key=f"n_{d}", help=f"Ніч з {d} на {d+timedelta(days=1)}"):
            st.session_state.active_nights[d] = not is_active
            st.rerun()
        # Застосовуємо колір через зміну стилю кнопки (Streamlit hack)
        # Оскільки st.button не має параметра class, ми "підсвічуємо" через стан
    col_ptr += 1
# Останній кілочок дати
with cols[col_ptr]:
    st.markdown(f"<div class='date-point'>{end_dt.strftime('%d.%m')}</div>", unsafe_allow_html=True)
# 3. ЛЕГЕНДА ТА РЕЗУЛЬТАТ
st.write("---")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("🔘 **Сірий** — Власні кошти / Приймаюча сторона")
with c2:
    st.markdown("🟢 **Зелений** — Оплачує ДСНС ($120)")
# Розрахунок загальної суми
total_sum = sum(120 for status in st.session_state.active_nights.values() if status)
st.metric("Загальна сума за проживання:", f"{total_sum} $")
if total_sum > 0:
    st.info("💡 Ці дані будуть автоматично перенесені у Таблицю 1 вашого кошторису.")
# Щоб візуально кнопки ставали зеленими/сірими, ми додамо невеликий інжект стилів для кожної кнопки окремо
style_inject = ""
for d, active in st.session_state.active_nights.items():
    bg_color = "#22c55e" if active else "#e2e8f0"
    txt_color = "white" if active else "#64748b"
    style_inject += f"""
        div.stButton > button[key="btn_n_{d}"] {{
            background-color: {bg_color} !important;
            color: {txt_color} !important;
        }}
