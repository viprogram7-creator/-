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
        padding: 5px;
        border-radius: 8px;
        min-width: 60px;
    }
    .night-container {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }
    </style>
    """, unsafe_allow_html=True)
st.title("🌙 Візуальна схема ночівель")
st.info("Натисніть на кнопку 'Ніч', щоб змінити її статус. Зелений колір = оплата ДСНС.")
# 1. Налаштування дат (можна буде змінювати)
start_dt = date(2026, 2, 1)
end_dt = date(2026, 2, 9)
# Створюємо список початкових дат для ночей
night_starts = []
curr = start_dt
while curr < end_dt:
    night_starts.append(curr)
    curr += timedelta(days=1)
# Ініціалізація стану кнопок у пам'яті програми
if 'active_nights' not in st.session_state:
    st.session_state.active_nights = {str(d): False for d in night_starts}
# 2. ПОБУДОВА СХЕМИ (Рядок: Дата -> Ніч -> Дата)
# Розраховуємо кількість колонок для горизонтального вигляду
cols = st.columns(len(night_starts) * 2 + 1)
for i, d in enumerate(night_starts):
    # Відображаємо дату
    with cols[i * 2]:
        st.markdown(f"<div class='date-label'>{d.strftime('%d.%m')}</div>", unsafe_allow_html=True)
    # Відображаємо кнопку ночі між датами
    with cols[i * 2 + 1]:
        d_str = str(d)
        is_active = st.session_state.active_nights[d_str]      
        # Якщо активовано - кнопка стає зеленою (primary), якщо ні - сірою (secondary)
        btn_type = "primary" if is_active else "secondary"      
        if st.button("Ніч", key=f"btn_{d_str}", type=btn_type, use_container_width=True):
            st.session_state.active_nights[d_str] = not is_active
            st.rerun()
# Відображаємо останню дату в кінці схеми
with cols[-1]:
    st.markdown(f<div class='date-label'>{end_dt.strftime('%d.%m')}</div>", unsafe_allow_html=True)
# 3. ПІДСУМОК ТА ТАБЛИЦЯ
st.write("---")
active_count = sum(st.session_state.active_nights.values())
total_cost = active_count * 120
c1, c2 = st.columns(2)
with c1:
    st.metric("Обрано ночівель:", active_count)
with c2:
    st.metric("Сума до виплати (ДСНС):", f"{total_cost} $")
if active_count > 0:
    st.success("✅ Ці дані будуть використані для формування Таблиці 1.")
    
    # Показуємо, як це виглядатиме в таблиці
    st.write("**Попередній вигляд рядків таблиці:**")
    results = []
    for d_str, active in st.session_state.active_nights.items():
        if active:
            results.append({"Дата початку ночі": d_str, "Країна": "Польща", "Сума": "120 $"})
    st.table(results)
