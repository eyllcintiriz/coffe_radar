import time
import requests
import streamlit as st
import sqlite3
from yelp_cafes import display_cafes_on_map
from streamlit_javascript import st_javascript
import geocoder

# Favori kafeyi veritabanina ekle
def add_favorite_cafe(user_id, cafe_name):
    if not is_cafe_in_favorites(user_id, cafe_name):  # Favorilerde değilse ekle
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO favorite_cafes (user_id, cafe_name) VALUES (?, ?)", (user_id, cafe_name))
        conn.commit()
        conn.close()
        st.info(f"{cafe_name} favorilere eklendi!")

# Kullanıcının favorilerinde olup olmadığını kontrol et
def is_cafe_in_favorites(user_id, cafe_name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM favorite_cafes WHERE user_id = ? AND cafe_name = ?", (user_id, cafe_name))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Kullanıcı ID'sini al
def get_user_id(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None
import streamlit as st
import sqlite3
import time
from db_helpers import get_user_id, add_favorite_cafe, is_cafe_in_favorites

# Kafeler listesini getir
def get_cafes():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM cafes")
    cafes = cursor.fetchall()
    conn.close()
    return [cafe[0] for cafe in cafes]

# Seçilen kafenin detaylarını getir
def get_cafe_details(cafe_name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT location, features FROM cafes WHERE name = ?", (cafe_name,))
    details = cursor.fetchone()
    conn.close()
    return details

# Ana sayfa
def main_page():
    st.title("Cafes Near You")

    # IP-based geolocation
    g = geocoder.ip('me')
    if g.ok and g.latlng:
        latitude, longitude = g.latlng
        display_cafes_on_map(latitude, longitude)
    else:
        st.error("Unable to determine your location via IP address.")

    # User can still search for another location
    st.subheader("Search for another location")
    location = st.text_input("Enter a location", "")
    if st.button("Search"):
        # Use geocoding to get latitude and longitude from location
        geocode_url = f"https://nominatim.openstreetmap.org/search?format=json&q={location}"
        headers = {'User-Agent': 'CoffeeRadar/1.0 (your_email@example.com)'}
        # response = requests.get(geocode_url, headers=headers)
        response = [{'lat': '0', 'lon': '0'}]  # Mock response for testing
        if response.status_code == 200:
            # geocode_data = response.json()
            geocode_data = response
            if geocode_data:
                latitude = float(geocode_data[0]['lat'])
                longitude = float(geocode_data[0]['lon'])
                display_cafes_on_map(latitude, longitude, location_name=location)
            else:
                st.error("Location not found.")
        else:
            st.error(f"Error fetching data: {response.status_code}")

# login_page.py
import streamlit as st
import sqlite3

# Kullanıcı doğrulama
def authenticate(username, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

# Giriş ekranı
def login_page():
    st.title("Giriş Yap")
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    if st.button("Giriş Yap"):
        user = authenticate(username, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"Merhaba, {username}! Yönlendiriliyorsunuz...")
            time.sleep(3)
            st.rerun()  # Force rerun to update UI
        else:
            st.error("Kullanıcı adı veya şifre hatalı!")
    st.markdown(f"<h1 style='text-align: center;'>Merhaba, {st.session_state['username']}! ☺️</h1>", unsafe_allow_html=True)
    
    st.title("Kafeler")
    
    cafes = get_cafes()
    user_id = get_user_id(st.session_state["username"])
    
    if cafes:
        for cafe in cafes:
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.image("https://via.placeholder.com/150", width=100)
            with col2:
                st.subheader(cafe)
            with col3:
                if not is_cafe_in_favorites(user_id, cafe):
                    if st.button(f"Favorilere Ekle: {cafe}", key=f"add_{cafe}"):
                        add_favorite_cafe(user_id, cafe)
                        st.success(f"{cafe} favorilere eklendi!")
                        time.sleep(2)
                        st.rerun()
                else:
                    st.caption("Zaten favorilerde")
    else:
        st.info("Kafeler yükleniyor...")
    
    st.subheader("Kafeleri İncele")
    if cafes:
        selected_cafe = st.selectbox("Bir kafe seçin", cafes)
        if selected_cafe:
            details = get_cafe_details(selected_cafe)
            if details:
                st.write(f"**Kafe Adı**: {selected_cafe}")
                st.write(f"**Konum**: {details[0]}")
                st.write(f"**Özellikler**: {details[1]}")
