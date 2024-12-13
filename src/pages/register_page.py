import streamlit as st
import sqlite3

# Kullanıcı ekleme
def add_user(username, password, email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password, email)
            VALUES (?, ?, ?)
        """, (username, password, email))
        conn.commit()
    except sqlite3.IntegrityError:
        st.error("Bu kullanıcı adı zaten alınmış!")
    conn.close()

# Kayıt ol sayfası
def register_page():
    st.title("Kayıt Ol")
    
    with st.form("register_form"):
        username = st.text_input("Kullanıcı Adı")
        password = st.text_input("Şifre", type="password")
        email = st.text_input("E-posta Adresi")
        submitted = st.form_submit_button("Kayıt Ol")
    
    if submitted:
        if username and password and email:
            add_user(username, password, email)
            st.success("Kayıt başarılı! Giriş yapmak için lütfen giriş ekranına gidin.")
        else:
            st.error("Tüm alanları doldurmanız gerekiyor!")
