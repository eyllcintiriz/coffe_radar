import streamlit as st
from login_page import login_page
from main_page import main_page
from favorite_cafes import favorite_cafes_page
from register_page import register_page

# Oturum durumunu kısmı
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "main"

# Sidebar sayfa geçişleri
if st.session_state["logged_in"]:
    st.sidebar.title("Sayfalar")
    page = st.sidebar.radio(
        "Geçiş Yap:",
        options=["Ana Sayfa", "Favori Kafeler"],
        index=0 if st.session_state["page"] == "main" else
              1 if st.session_state["page"] == "favorite_cafes" else 0,
    )
    st.session_state["page"] = page

    if st.sidebar.button("Çıkış Yap"):
        st.session_state["logged_in"] = False
        st.session_state["page"] = "main"
        st.rerun()  # Force rerun to update UI

    # Seçime göre sayfa çağırma
    if st.session_state["page"] == "Ana Sayfa":
        main_page()
    elif st.session_state["page"] == "Favori Kafeler":
        favorite_cafes_page()

else:
    auth_option = st.sidebar.radio("Seçiminizi Yapın", ["Giriş Yap", "Kayıt Ol"])
    if auth_option == "Giriş Yap":
        login_page()
    else:
        register_page()

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
