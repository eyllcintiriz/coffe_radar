# register_page.py
import streamlit as st
import sqlite3

def register_page():
    st.title("Kayıt Ol")
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    confirm_password = st.text_input("Şifreyi Onayla", type="password")
    
    if st.button("Kayıt Ol"):
        if password != confirm_password:
            st.error("Şifreler eşleşmiyor!")
        elif not username or not password:
            st.error("Kullanıcı adı ve şifre gerekli!")
        else:
            try:
                conn = sqlite3.connect("users.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                conn.close()
                st.success("Kayıt başarılı! Giriş yapabilirsiniz.")
            except sqlite3.IntegrityError:
                st.error("Bu kullanıcı adı zaten alınmış!")