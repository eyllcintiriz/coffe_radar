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