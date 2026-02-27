import streamlit as st
import pandas as pd
from datetime import timedelta, date
st.title("🏨 Розрахунок проживання")
# Визначаємо період (у реальному коді це буде з вашої Сторінки 1)
start_dt = date(2026, 2, 1)
end_dt = date(2026, 2, 9)
all_days = [start_dt + timedelta(days=x) for x in range((end_total-start_total).days + 1)]
# Перетворюємо дати у зручний для читання текст
date_options = [d.strftime("%d.%m.%Y") for d in all_days]
# ВІЗУАЛЬНИЙ ВИБІР: Користувач просто обирає дати зі списку доступних
st.subheader("Оберіть дати ночівель, які покриває ДСНС:")
selected_nights = st.multiselect("Можна обрати декілька:", options=date_options)
if selected_nights:
    st.info(f"✅ ДСНС покриває найм житла за наступні дати: {', '.join(selected_nights)}")
# АВТОМАТИЧНА ТАБЛИЦЯ
table_data = []
for d_str in date_options:
    cost = "120 доларів" if d_str in selected_nights else "-"
    table_data.append({"Дата": d_str, "Країна": "Польща", "Витрати ДСНС": cost})
st.table(pd.DataFrame(table_data))
