import streamlit as st
from datetime import timedelta, date
st.set_page_config(layout="wide", page_title="Схема ночівель ДСНС")
# Стилізація для дат та контейнера
st.markdown("""
    <style>
    .date-label {
        text-align: center;
        font-weight: bold;
        color: #1e3a8a;
        background-color: #e2e8f0;
        padding: 8px;
        border-radius: 8px;
        min-width: 70px;
        font-size: 14px;
    }
    /* Вирівнювання кнопок по центру відносно дат */
    .stButton > button {
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("🌙 Візуальна схема ночівель")
st.info("Кожна кнопка — це ніч між двома датами. Зелений колір = витрати покриває ДСНС.")
# 1. Налаштування дат
start_dt = date(2026, 2, 1)
end_dt = date(2026, 2, 9)
# Створюємо список початкових дат для ночей
night_starts = []
curr = start_dt
while curr < end_dt:
    night_starts.append(curr)
    curr += timedelta(days=1)
# Ініціалізація стану кнопок
if 'active_nights' not in st.session_state:
    st.session_state.active_nights = {str(d): False for d in night_starts}
# 2. ПОБУДОВА СХЕМИ
# Створюємо колонки (кількість ночей * 2 + 1 для останньої дати)
cols = st.columns(len(night_starts) * 2 + 1)
for i, d in enumerate(night_starts):
    # Відображаємо дату
    with cols[i * 2]:
        st.markdown(f"<div class='date-label'>{d.strftime('%d.%m')}</div>", unsafe_allow_html=True)
    # Відображаємо кнопку ночі
    with cols[i * 2 + 1]:
        d_str = str(d)
        is_active = st.session_state.active_nights[d_str]    
        # Зелена (primary) якщо обрано, сіра (secondary) якщо ні
        btn_type = "primary" if is_active else "secondary"   
        if st.button("Ніч", key=f"btn_{d_str}", type=btn_type, use_container_width=True):
            st.session_state.active_nights[d_str] = not is_active
            st.rerun()
# Відображаємо останню дату (Кінець відрядження)
with cols[-1]:
    st.markdown(f"<div class='date-label'>{end_dt.strftime('%d.%m')}</div>", unsafe_allow_html=True)
# 3. РЕЗУЛЬТАТИ
st.write("---")
active_count = sum(st.session_state.active_nights.values())
total_cost = active_count * 120
col_m1, col_m2 = st.columns(2)
col_m1.metric("Кількість оплачених ночей", active_count)
col_m2.metric("Сума до відшкодування", f"{total_cost} $")
if active_count > 0:
    st.success("📊 Дані готові для заповнення таблиці 1.")  
    # Формуємо список обраних дат для наочності
    selected_list = [d_str for d_str, active in st.session_state.active_nights.items() if active]
    st.write(f"Обрані ночі (початок): {', '.join(selected_list
