import sqlite3
import streamlit as st
from db_helpers import send_password_reset_email

def forgot_password_page():
    st.title("Şifremi Unuttum")
    email = st.text_input("Email")
    if st.button("Şifre Sıfırlama Linki Gönder"):
        # Fetch username associated with the email
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        conn.close()
        if result:
            username = result[0]
            send_password_reset_email(email, username)
            st.success("Şifre sıfırlama linki email adresinize gönderildi.")
        else:
            st.error("Bu email adresiyle kayıtlı kullanıcı bulunamadı.")