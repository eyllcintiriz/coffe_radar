import streamlit as st
import sqlite3

# Kullanıcının favori kafelerini getir
def get_favorite_cafes(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT cafe_name FROM favorite_cafes WHERE user_id = ?", (user_id,))
    cafes = cursor.fetchall()
    conn.close()
    return [cafe[0] for cafe in cafes]

# Favori kafeyi veritabanından sil
def remove_favorite_cafe(user_id, cafe_name):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorite_cafes WHERE user_id = ? AND cafe_name = ?", (user_id, cafe_name))
    conn.commit()
    conn.close()
    st.session_state["page"] = "favorite_cafes"  # Sayfayı güncellemek için durumu değiştir
    st.session_state["update"] = not st.session_state.get("update", False)  # Durum tetikleyicisi
    st.info(f"{cafe_name} favorilerden çıkarıldı!")

# Kullanıcı ID'sini al
def get_user_id(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()
    conn.close()
    return user_id[0] if user_id else None

# Favori kafeler sayfası
def favorite_cafes_page():
    st.title("Favori Kafeleriniz")
    
    user_id = get_user_id(st.session_state["username"])
    cafes = get_favorite_cafes(user_id)
    
    if cafes:
        for cafe in cafes:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(cafe)
            with col2:
                if st.button(f"Favorilerden Çıkar: {cafe}", key=f"remove_{cafe}"):
                    remove_favorite_cafe(user_id, cafe)
    else:
        st.info("Henüz favori kafe eklemediniz.")
