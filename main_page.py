import streamlit as st
import sqlite3

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
    # Büyük karşılama mesajı
    st.markdown(f"<h1 style='text-align: center;'>Merhaba, {st.session_state['username']}! ☺️</h1>", unsafe_allow_html=True)
    
    # Başlık
    st.title("Kafeler")
    
    # Kafeler Listesi
    cafes = get_cafes()
    user_id = get_user_id(st.session_state["username"])
    

    # image api üzerinden çekilecek ve kafeler listesine eklenecek!!!
    #kafeler listesi init_db.py de var
    # DAHA YAPILMADI
    if cafes:
        for cafe in cafes:
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.image("https://via.placeholder.com/150", width=100)
            with col2:
                st.subheader(cafe)
            with col3:
                if not is_cafe_in_favorites(user_id, cafe):  # Favorilerde değilse göster
                    if st.button(f"Favorilere Ekle: {cafe}", key=f"add_{cafe}"):
                        add_favorite_cafe(user_id, cafe)
                else:
                    st.caption("Zaten favorilerde")
    else:
        st.info("Kafeler yükleniyor...")
    
    # İnceleme Bölümü
    st.subheader("Kafeleri İncele")
    if cafes:
        selected_cafe = st.selectbox("Bir kafe seçin", cafes)
        if selected_cafe:
            details = get_cafe_details(selected_cafe)
            if details:
                st.write(f"**Kafe Adı**: {selected_cafe}")
                st.write(f"**Konum**: {details[0]}")
                st.write(f"**Özellikler**: {details[1]}")
