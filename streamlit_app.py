import streamlit as st
import pandas as pd

# Налаштування сторінки
st.set_page_config(page_title="Розрахунок відряджень", page_icon="💰")

def calculate_allowance():
    st.title("💰 Експертна система розрахунку відряджень")
    st.divider()

    # Питання 1
    st.subheader("1. Тип витрат")
    location_label = st.radio(
        "Оберіть місце відрядження:",
        ["По Україні (1)", "За кордон (2)"],
        index=0
    )
    location = "1" if "По Україні" in location_label else "2"

    # Питання 2
    if location == "2":
        country = st.text_input("2. Введіть країну призначення:", placeholder="Наприклад: Польща")
    else:
        country = "Україна"

    # Питання 3
    st.subheader("2. Тип заходу")
    reason_label = st.selectbox(
        "Оберіть тип заходу:",
        ["Зустріч (1)", "Навчання (2)", "Практичний тренінг (3)"]
    )
    reason_code = reason_label.split("(")[1][0] # беремо цифру з дужок

    # Логіка відсотків
    percentage = 1.0
    if reason_code == "2":
        percentage = 0.8
        st.info("ℹ️ Система: Застосовано коефіцієнт 80% (Навчання)")

    # Питання 4
    st.subheader("3. Термін")
    days = st.number_input("Введіть загальну кількість днів відрядження:", min_value=1, max_value=200, value=1)

    if days > 90:
        st.error("❌ ПОМИЛКА: Згідно з Постановою, відрядження не може тривати понад 90 днів.")
        st.stop() # Зупиняємо програму

    # Питання 5: Детальне опитування
    st.subheader("4. Деталі по днях")
    daily_data = []
    base_rate = 300 if location == "1" else 2500 # Приклад суми

    with st.expander("Натисніть, щоб заповнити дані по днях"):
        for day in range(1, int(days) + 1):
            st.write(f"📅 *День {day}*")
            city = st.text_input(f"Місто перебування (день {day}):", key=f"city_{day}")
            food = st.radio(
                f"Харчування у цей добу:",
                ["Ні (0)", "1-разове (1)", "2-разове (2)"],
                key=f"food_{day}"
            )
            daily_data.append({"day": day, "city": city, "food": food})

    # Фінальний розрахунок
    if st.button("📊 Розрахувати підсумок"):
        st.divider()
        st.balloons()
        st.success("Розрахунок завершено!")
        
        total_sum = days * base_rate * percentage
        st.metric(label="Загальна сума добових", value=f"{total_sum} грн")
        
        st.write(f"*Деталі:*")
        st.write(f"- Напрямок: {country}")
        st.write(f"- Кількість днів: {days}")
        st.write(f"- Коефіцієнт: {percentage*100}%")

# Запуск функції
if _name_ == "_main_":
    calculate_allowance()
