import streamlit as st
from datetime import datetime
st.set_page_config(page_title="Перевірка відрядження")
# Ініціалізація стану
if "page" not in st.session_state:
    st.session_state.page = 1
if "days" not in st.session_state:
    st.session_state.days = None
# -------------------
# Сторінка 1
# -------------------
if st.session_state.page == 1:
    st.title("Питання 1")
    days = st.number_input("Скільки днів відрядження?", min_value=1, step=1)
    if st.button("Далі"):
        st.session_state.days = days
        if days > 90:
            st.session_state.page = "warning"
        else:
            st.session_state.page = 2
        st.rerun()
# -------------------
# Сторінка попередження (>90)
# -------------------
elif st.session_state.page == "warning":
    st.title("Попередження")
    st.error("Відрядження на навчання більше 90 днів не може бути, відповідно до §287 Постанови КМУ (параграф 1).")
    st.markdown("[Переглянути Постанову КМУ №287](https://zakon.rada.gov.ua/laws/show/287-2011-%D0%BF)")
    if st.button("Повернутися назад"):
        st.session_state.page = 1
        st.rerun()
# -------------------
# Сторінка 2
# -------------------
elif st.session_state.page == 2:
    st.title("Питання 2")
    st.write(f"Вказана кількість днів: **{st.session_state.days}**")
    date_from = st.date_input("Дата 'з'")
    date_to = st.date_input("Дата 'по'")
   if st.button("Перевірити"):
    if date_to < date_from:
        st.error("Дата 'по' не може бути раніше дати 'з'")
    else:
        actual_days = (date_to - date_from).days + 1
        if actual_days != st.session_state.days:
            st.error(
                f"Термін відрядження не збігається з кількістю днів! "
                f"За датами виходить {actual_days} днів.")
        else:
            st.success("Дані введені правильно ✅")
