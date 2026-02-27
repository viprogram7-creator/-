import streamlit as st
import pandas as pd
from datetime import timedelta, date
st.set_page_config(page_title="ДСНС - Розрахунок", layout="centered")
st.title("🏨 Вибір проживання (ДСНС)")
# 1. Визначаємо період (ці дані зазвичай приходять з минулої сторінки)
start_dt = date(2026, 2, 1)
end_dt = date(2026, 2, 9)
# Розраховуємо список усіх дат відрядження без помилок
# (Кількість днів = різниця між датами + 1)
num_days = (end_dt - start_dt).days + 1
all_days = [start_dt + timedelta(days=x) for x in range(num_days)]
# Перетворюємо дати у зручний текст для списку
date_options = [d.strftime("%d.%m.%Y") for d in all_days]
st.info(f"Відрядження триває з {start_dt.strftime('%d.%m')} по {end_dt.strftime('%d.%m')}")
# 2. ВІЗУАЛЬНИЙ ВИБІР: Користувач обирає дати зі списку
st.subheader("Оберіть дати ночівель, які покриває ДСНС:")
selected_nights = st.multiselect(
    "Клацніть, щоб обрати одну або декілька дат:",
    options=date_options,
    help="Оберіть тільки ті дати, за які проживання оплачує держава"
)
# 3. АВТОМАТИЧНА ТАБЛИЦЯ
st.write("---")
st.subheader("Таблиця 1: Попередній розрахунок")
table_data = []
for d in all_days:
    d_str = d.strftime("%d.%m.%Y")
    # Перевірка: чи є ця дата у списку обраних
    cost = "120 доларів" if d_str in selected_nights else "-"
    table_data.append({
        "Дата": d_str,
        "Країна": "Польща",
        "Витрати на житло (ДСНС)": cost
    })
# Відображення таблиці
df = pd.DataFrame(table_data)
st.dataframe(df, use_container_width=True)
if selected_nights:
    st.success(f"✅ Ви обрали {len(selected_nights)} ночей для оплати ДСНС.")
