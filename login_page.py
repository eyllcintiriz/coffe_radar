import time
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
            time.sleep(1)
            st.rerun()  # Force rerun to update UI
        else:
            st.error("Kullanıcı adı veya şifre hatalı!")

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
                st.rerun()  # Optionally rerun to show login page
            except sqlite3.IntegrityError:
                st.error("Bu kullanıcı adı zaten alınmış!")
