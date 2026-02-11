import streamlit as st
import pandas as pd
from io import BytesIO

# Налаштування сторінки
st.set_page_config(page_title="Калькулятор відряджень", page_icon="💼")

st.title("💼 Розрахунок кошторису на відрядження")
st.markdown("""
Цей інструмент допоможе правильно розрахувати добові згідно з чинним законодавством.
""")

# --- ПИТАННЯ 1 & 2: Напрямок ---
st.header("1. Основна інформація")

col1, col2 = st.columns(2)

with col1:
    location = st.radio(
        "Напрямок відрядження:",
        ["По Україні", "За кордон"],
        help="Від цього залежить базова ставка добових та валюта розрахунку."
    )

with col2:
    if location == "За кордон":
        country = st.text_input("Введіть країну:", "Польща")
    else:
        country = "Україна"
        st.info("Ставка зафіксована для України.")

# --- ПИТАННЯ 3: Мета (Постанова) ---
st.subheader("Мета відрядження")
reason = st.selectbox(
    "Оберіть тип заходу:",
    ["Робоча зустріч", "Навчання", "Тренінг", "Практичний тренінг"],
    help="Тип заходу впливає на відсоток виплати добових (згідно з Постановою №...)"
)

# Відображення довідки залежно від вибору
if reason == "Навчання":
    st.warning("ℹ️ **Довідка:** Для навчання застосовується знижений коефіцієнт (наприклад, 80%). [Див. абзац 2 ст. 4]")
    coeff = 0.8
else:
    coeff = 1.0

# --- ПИТАННЯ 4: Термін ---
days_count = st.number_input("Кількість днів відрядження:", min_value=1, max_value=200, value=1)

if days_count > 90:
    st.error("❌ **Увага!** Відрядження понад 90 днів неможливе згідно з чинним законодавством. Будь ласка, перевірте терміни.")
    st.stop() # Зупиняє програму, якщо порушено закон

# --- ПИТАННЯ 5: Деталізація по днях ---
st.header("2. Деталізація по днях")
st.write("Заповніть дані для кожного дня відрядження:")

rows = []
for i in range(int(days_count)):
    with st.expander(f"День {i+1}", expanded=(i == 0)):
        c1, c2, c3 = st.columns(3)
        
        with c1:
            city = st.text_input(f"Місто перебування", key=f"city_{i}")
        with c2:
            arrival = st.checkbox(f"Перетин кордону/прибуття", key=f"arr_{i}")
        with c3:
            food = st.selectbox(
                "Харчування (в готелі):",
                ["Не включено", "1-разове", "2-разове", "3-разове"],
                key=f"food_{i}"
            )
        
        # Логіка розрахунку (прикладна)
        base_rate = 710 if location == "По Україні" else 80 # Приклад: грн або євро
        current_rate = base_rate * coeff
        
        if food == "1-разове": current_rate *= 0.8
        elif food == "2-разове": current_rate *= 0.6
        elif food == "3-разове": current_rate *= 0.3
        
        rows.append({
            "День": i + 1,
            "Місто": city,
            "Перетин кордону": "Так" if arrival else "Ні",
            "Харчування": food,
            "Розрахована сума": round(current_rate, 2)
        })

# --- РЕЗУЛЬТАТ ---
st.header("3. Результат розрахунку")

df = pd.DataFrame(rows)
st.table(df)

total_sum = df["Розрахована сума"].sum()
st.metric("Загальна сума добових:", f"{total_sum} {'грн' if location == 'По Україні' else 'од.'}")

# --- ЕКСПОРТ В EXCEL ---
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

excel_data = to_excel(df)
st.download_button(
    label="📥 Скачати готовий Excel-файл",
    data=excel_data,
    file_name="koshtoris_vidryadzhennya.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
