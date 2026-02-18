import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
# 1. Словник-перекладач (додайте сюди потрібні країни)
TRANSLATIONS = {
    "Ukraine": "Україна",
    "United Kingdom": "Велика Британія",
    "Poland": "Польща",
    "Germany": "Німеччина",
    "France": "Франція",
    "Italy": "Італія",
    "Spain": "Іспанія",
    "Slovakia": "Словаччина",
    "Hungary": "Угорщина",
    "Romania": "Румунія",
    "Moldova": "Молдова",
    "Czechia": "Чехія",
    "United States of America": "США",
    "Turkey": "Туреччина"
}
def get_ukrainian_name(english_name):
    # Повертає українську назву, якщо вона є в словнику, інакше залишає англійську
    return TRANSLATIONS.get(english_name, english_name)
# --- Налаштування сторінки ---
if 'selected_countries' not in st.session_state:
    st.session_state.selected_countries = []
st.title("🗺️ Вибір країни (Українською)")
# Відображення списку вже обраних країн
if st.session_state.selected_countries:
    st.write("**Обрані країни:**")
    for c in st.session_state.selected_countries:
        st.info(f"📍 {c}")
# Створення карти
m = folium.Map(location=[50, 20], zoom_start=3, tiles="CartoDB positron")
# Завантаження геоданих
geo_json_url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
geo_data = requests.get(geo_json_url).json()
# Додаємо українські назви в дані карти перед відображенням
for feature in geo_data['features']:
    eng_name = feature['properties']['name']
    feature['properties']['name_ua'] = get_ukrainian_name(eng_name)
# Малюємо карту
folium.GeoJson(
    geo_data,
    style_function=lambda x: {'fillColor': '#004aad', 'color': 'white', 'weight': 1, 'fillOpacity': 0.2},
    highlight_function=lambda x: {'fillColor': '#00d4ff', 'fillOpacity': 0.6},
    # ТЕПЕР ПІДКАЗКА БУДЕ УКРАЇНСЬКОЮ
    tooltip=folium.GeoJsonTooltip(fields=['name_ua'], aliases=['Країна:'])
).add_to(m)
# Обробка кліку
map_output = st_folium(m, width=700, height=400)
if map_output and map_output.get("last_active_drawing"):
    # Отримуємо саме українську назву з властивостей об'єкта, на який натиснули
    selected_ua = map_output["last_active_drawing"]["properties"]["name_ua"]
    if selected_ua not in st.session_state.selected_countries:
        if len(st.session_state.selected_countries) < 3:
            st.session_state.selected_countries.append(selected_ua)
            st.rerun()
