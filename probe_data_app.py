import streamlit as st
import pandas as pd
from datetime import date, timedelta
# --- Налаштування стилів ---
st.markdown("""
    <style>
    .night-card {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        cursor: pointer;
        border: 2px solid #555;
        transition: 0.3s;
    }
    .night-card.active {
        background: #2e7d32 !important;
        border: 2px solid #a5d6a7;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("🌙 Планування відрядження")
# --- Дані ---
start_date = date(2026, 2, 1)
end_date = date(2026, 2, 9)
# Ночівлі в ніч з (1 на 2) по (6 на 7)
night_dates = [date(2026, 2, i) for i in range(2, 8)]
if 'nights' not in st.session_state:
    st.session_state.nights = {d: False for d in night_dates}
# --- Відображення терміну ---
st.subheader("Загальний термін відрядження: 01.02.2026 – 09.02.2026")
# Відображення дат та кнопок ночівлі
cols = st.columns(len(night_dates) * 2 + 1)
curr_date = start_date
for i in range((end_date - start_date).days + 1):
    d = start_date + timedelta(days=i)
    cols[i*2].write(f"**{d.strftime('%d.%m')}**")
    # Якщо це дата після якої є "ночівля"
    if d in night_dates:
        is_active = st.session_state.nights[d]
        css_class = "night-card active" if is_active else "night-card" 
        # Кнопка ночівлі
        if st.button(f"🌙✨ НОЧІВЛЯ", key=f"n_{d}"):
            st.session_state.nights[d] = not is_active
            if not is_active:
                st.toast("Витрати на найм житлового приміщення покриває ДСНС!", icon="🏨")
           st.rerun()
# --- Таблиця 1 ---
st.markdown("---")
st.subheader("Таблиця 1")
table_data = []
for i in range((end_date - start_date).days + 1):
    d = start_date + timedelta(days=i)
    # Якщо ночівля була активна
    cost = 120 if st.session_state.nights.get(d, False) else 0
    table_data.append({
        "Дата": d.strftime("%d.%m.%Y"),
        "Країна": "Польща",
        "Добові (USD)": cost if cost > 0 else "-"
    })
df = pd.DataFrame(table_data)
st.table(df)
if st.button("🔄 Почати заново"):
    st.session_state.nights = {d: False for d in night_dates}
    st.rerun()
