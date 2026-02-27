import streamlit as st
from datetime import timedelta, date
st.set_page_config(layout="wide", page_title="Схема ночівель ДСНС")
# Стилізація для візуального ряду
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
        border: 1px solid #cbd5e1;
    }
    .stButton > button {
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("🌙 Візуальна схема ночівель")
st.info("Кожна кнопка — це ніч. Зелений колір означає, що проживання оплачує ДСНС.")
# 1. Налаштування дат
start_dt = date(2026, 2, 1)
end_dt = date(2026, 2, 9)
# Створюємо список початкових дат для ночей
night_starts = []
curr = start_dt
while curr < end_dt:
    night_starts.append(curr)
    curr += timedelta(days=1)
# Ініціалізація стану кнопок у пам'яті
if 'active_nights' not in st.session_state:
    st.session_state.active_nights = {str(d): False for d in night_starts}
# 2. ПОБУДОВА ВІЗУАЛЬНОЇ СХЕМИ
# Створюємо колонки (кількість ночей * 2 + 1)
cols = st.columns(len(night_starts) * 2 + 1)
for i, d in enumerate(night_starts):
    # Відображаємо дату (кілочок)
    with cols[i * 2]:
        st.markdown(f"<div class='date-label'>{d.strftime('%d.%m')}</div>", unsafe_allow_html=True) 
    # Відображаємо кнопку ночі між датами
    with cols[i * 2 + 1]:
        d_str = str(d)
        is_active = st.session_state.active_nights[d_str]     
        # Тип кнопки: primary (синій/зелений залежно від теми) або secondary (сірий)
        btn_type = "primary" if is_active else "secondary"       
        # Підказка при наведенні
        help_text = f"Ніч з {d.strftime('%d.%m')} на {(d + timedelta(days=1)).strftime('%d.%m')}"       
        if st.button("Ніч", key=f"btn_{d_str}", type=btn_type, use_container_width=True, help=help_text):
            st.session_state.active_nights[d_str] = not is_active
            st.rerun()
# Відображаємо останню дату
with cols[-1]:
    st.markdown(f"<div class='date-label'>{end_dt.strftime('%d.%m')}</div>", unsafe_allow_html=True)
# 3. РЕЗУЛЬТАТИ ТА РОЗРАХУНОК
st.write("---")
active_count = sum(st.session_state.active_nights.values())
total_cost = active_count * 120  # Базова сума, яку ми замінимо на логіку з файлу
col_m1, col_m2 = st.columns(2)
col_m1.metric("Кількість обраних ночей", active_count)
col_m2.metric("Загальна сума проживання", f"{total_cost} $")
if active_count > 0:
    st.success("✅ Схема сформована. Дані готові для заповнення кошторису.")   
    # Список обраних ночей для перевірки
    selected_list = [f"з {d_str}" for d_str, active in st.session_state.active_nights.items() if active]
    st.write(f"**Обрані ночі:** {', '.join(selected_list)}")
