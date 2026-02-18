import streamlit as st
from streamlit_folium import st_folium
import folium
import json
import requests
# Налаштування сторінки
st.set_page_config(page_title="Travel Designer", page_icon="🗺️")
# Стилізація (Ділово-мультяшна)
st.markdown("""
    <style>
    .stButton>button {
        border-radius: 20px;
        background-color: #004aad;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #00d4ff;
        color: black;
    }
    .country-tag {
        display: inline-block;
        padding: 5px 15px;
        margin: 5px;
        background-color: #e1f5fe;
        border: 2px solid #004aad;
        border-radius: 15px;
        color: #004aad;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)
# Ініціалізація стану
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'selected_countries' not in st.session_state:
    st.session_state.selected_countries = []
if 'show_map' not in st.session_state:
    st.session_state.show_map = False
def go_to(p):
    st.session_state.page = p
    st.rerun()
# --- СТОРІНКА 1 ---
if st.session_state.page == 1:
    st.title("📂 Початок оформлення")
    st.write("---")
    st.markdown("### Оберіть напрям відрядження:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇺🇦 а. Україна"):
            st.toast("Ця функція ще недоступна 🚧", icon="⚠️")
    with col2:
        if st.button("🌍 б. Закордон"):
            go_to(2)
# --- СТОРІНКА 2 ---
elif st.session_state.page == 2:
    st.title("🗺️ Вибір країн")
    st.write("---")
    st.markdown("### Оберіть країну відрядження:")
    st.caption("Ви можете обрати до 3-х країн, натиснувши на карту")
    # Відображення обраних країн
    if st.session_state.selected_countries:
        cols = st.columns(len(st.session_state.selected_countries))
        for idx, country in enumerate(st.session_state.selected_countries):
            with cols[idx]:
                st.markdown(f"<div class='country-tag'>📍 {country}</div>", unsafe_allow_html=True)
                if st.button(f"Видалити {country}", key=f"del_{idx}"):
                    st.session_state.selected_countries.pop(idx)
                    st.rerun()
    st.write("")
    # Кнопка "+" для виклику карти
    if len(st.session_state.selected_countries) < 3:
        if st.button("➕ Додати країну через карту"):
            st.session_state.show_map = not st.session_state.show_map
    # Карта (з'являється при натисканні на +)
    if st.session_state.show_map and len(st.session_state.selected_countries) < 3:
        st.info("Натисніть на країну на карті, щоб додати її")
        # Створення карти
        m = folium.Map(location=[50, 20], zoom_start=3, tiles="CartoDB positron")
        # Завантажуємо межі країн для клікабельності
        geo_json_data = requests.get(
            "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
        ).json()
        folium.GeoJson(
            geo_json_data,
            name="geojson",
            style_function=lambda x: {'fillColor': '#004aad', 'color': '#004aad', 'weight': 1, 'fillOpacity': 0.1},
            highlight_function=lambda x: {'fillColor': '#00d4ff', 'fillOpacity': 0.5},
            tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Країна:'])
        ).add_to(m)
        # Обробка кліку
        output = st_folium(m, width=700, height=400)
        if output and output.get("last_active_drawing"):
            new_country = output["last_active_drawing"]["properties"]["name"]
            if new_country not in st.session_state.selected_countries:
                st.session_state.selected_countries.append(new_country)
                st.session_state.show_map = False # Ховаємо карту після вибору
                st.rerun()
    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("⬅️ Назад"): go_to(1)
    with c2:
        if len(st.session_state.selected_countries) > 0:
            if st.button("Далі ➡️"): go_to(3)
# --- СТОРІНКА 3 ---
elif st.session_state.page == 3:
    st.title("✅ Крок 3")
    st.success(f"Ви обрали: {', '.join(st.session_state.selected_countries)}")
    if st.button("⬅️ Повернутися до карти"): go_to(2)
