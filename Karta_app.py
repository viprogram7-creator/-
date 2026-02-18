import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
# 1. Повний словник перекладів для країн (Постанова №98 + основні)
TRANSLATIONS = {
    "Ukraine": "Україна", "United Kingdom": "Велика Британія", "Poland": "Польща",
    "Germany": "Німеччина", "France": "Франція", "Italy": "Італія",
    "Spain": "Іспанія", "Slovakia": "Словаччина", "Hungary": "Угорщина",
    "Romania": "Румунія", "Moldova": "Молдова", "Czechia": "Чехія",
    "United States of America": "США", "Turkey": "Туреччина", "Austria": "Австрія",
    "Belgium": "Бельгія", "Bulgaria": "Болгарія", "Croatia": "Хорватія",
    "Cyprus": "Кіпр", "Denmark": "Данія", "Estonia": "Естонія",
    "Finland": "Фінляндія", "Greece": "Греція", "Ireland": "Ірландія",
    "Latvia": "Латвія", "Lithuania": "Литва", "Luxembourg": "Люксембург",
    "Malta": "Мальта", "Netherlands": "Нідерланди", "Portugal": "Португалія",
    "Slovenia": "Словенія", "Sweden": "Швеція", "Switzerland": "Швейцарія",
    "Canada": "Канада", "Georgia": "Грузія", "Israel": "Ізраїль",
    "Norway": "Норвегія", "Japan": "Японія", "China": "Китай"
}
# --- Ініціалізація стану ---
if 'selected_countries' not in st.session_state:
    st.session_state.selected_countries = []
st.title("🗺️ Оберіть країну відрядження")
st.markdown("Наведіть на країну, щоб побачити назву українською, та натисніть для вибору.")
# Відображення списку вже обраних країн
if st.session_state.selected_countries:
    cols = st.columns(len(st.session_state.selected_countries))
    for idx, c in enumerate(st.session_state.selected_countries):
        with cols[idx]:
            st.info(f"📍 {c}")
            if st.button(f"Видалити", key=f"del_{idx}"):
                st.session_state.selected_countries.pop(idx)
                st.rerun()
# --- ЛОГІКА КАРТИ ---
# Створюємо карту
m = folium.Map(location=[50, 20], zoom_start=3, tiles="CartoDB positron")
# Завантажуємо дані кордонів
geo_json_url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
geo_data = requests.get(geo_json_url).json()
# ВАЖЛИВО: Замінюємо англійські назви на українські всередині даних GeoJSON
for feature in geo_data['features']:
    eng_name = feature['properties']['name']
    # Якщо перекладу немає, залишаємо англійську назву
    ua_name = TRANSLATIONS.get(eng_name, eng_name)
    feature['properties']['name'] = ua_name  # Тепер 'name' для карти — це українська назва
# Додаємо шар GeoJson на карту
folium.GeoJson(
    geo_data,
    style_function=lambda x: {
        'fillColor': '#004aad', 
        'color': 'white', 
        'weight': 1, 
        'fillOpacity': 0.2
    },
    highlight_function=lambda x: {
        'fillColor': '#00d4ff', 
        'fillOpacity': 0.6,
        'weight': 2
    },
    # Відображаємо українську назву при наведенні
    tooltip=folium.GeoJsonTooltip(
        fields=['name'], 
        aliases=['Країна:'],
        localize=True
    )
).add_to(m)
# Рендеримо карту в Streamlit
map_output = st_folium(m, width=700, height=450)
# Обробка вибору країни
if map_output and map_output.get("last_active_drawing"):
    # Отримуємо назву (яка вже українська завдяки коду вище)
    selected_name = map_output["last_active_drawing"]["properties"]["name"]
    if selected_name not in st.session_state.selected_countries:
        if len(st.session_state.selected_countries) < 3:
            st.session_state.selected_countries.append(selected_name)
            st.rerun()
if len(st.session_state.selected_countries) >= 3:
    st.warning("Ви обрали максимальну кількість країн (3).")
if st.button("Далі до наступного кроку ➡️"):
    if st.session_state.selected_countries:
        st.success("Країни збережено!")
    else:
        st.error("Будь ласка, оберіть хоча б одну країну.")
