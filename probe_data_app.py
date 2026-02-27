import streamlit as st
import pandas as pd
from datetime import timedelta, date
st.set_page_config(page_title="ДСНС - Розрахунок ночівель", layout="centered")
st.title("🏨 Вибір ночівель")
# 1. Задаємо межі відрядження
start_dt = date(2026, 2, 1)
end_dt = date(2026, 2, 9)
st.info(f"📅 Період відрядження: з **{start_dt.strftime('%d.%m')}** по **{end_dt.strftime('%d.%m')}**")
# 2. Генеруємо проміжки "Ніч з... на..."
# Кількість ночей завжди на 1 менша, ніж кількість днів
night_options = []
all_days = []
curr = start_dt
while curr < end_dt:
    next_day = curr + timedelta(days=1)
    night_label = f"Ніч з {curr.strftime('%d.%m')} на {next_day.strftime('%d.%m')}"
    night_options.append(night_label)
    all_days.append(curr) # зберігаємо дату початку для логіки таблиці
    curr = next_day
# Додаємо останній день у список для повної таблиці
full_date_range = [start_dt + timedelta(days=x) for x in range((end_dt - start_dt).days + 1)]
# 3. Мультиселект для вибору ночей
st.subheader("Оберіть ночівлі, які покриває ДСНС:")
selected_nights = st.multiselect(
    "Оберіть один або кілька варіантів:",
    options=night_options,
    help="Кожен обраний проміжок додасть 120 доларів у таблицю"
)
# 4. Формування Таблиці 1
st.write("---")
st.subheader("Таблиця 1")
table_data = []
for d in full_date_range:
    d_str = d.strftime("%d.%m.%Y")
    # Визначаємо, чи була ця дата початком обраної ночі
    # Шукаємо, чи є в обраних ночах рядок, що починається з цієї дати
    is_covered = False
    for night in selected_nights:
        if f"з {d.strftime('%d.%m')}" in night:
            is_covered = True
            break
    cost = "120 доларів" if is_covered else "-"
    table_data.append({
        "Дата": d_str,
        "Країна": "Польща",
        "Проживання (ДСНС)": cost
    })
df = pd.DataFrame(table_data)
# Використовуємо стилізацію, щоб підсвітити заповнені рядки
def highlight_costs(s):
    return ['background-color: #e2f0d9' if v == "120 доларів" else '' for v in s]
st.dataframe(df.style.apply(highlight_costs, subset=['Проживання (ДСНС)']), use_container_width=True)
if selected_nights:
    st.success(f"✅ Узгоджено оплату проживання за {len(selected_nights)} ночі(ей).")
