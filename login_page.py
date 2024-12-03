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
        else:
            st.error("Kullanıcı adı veya şifre hatalı!")
