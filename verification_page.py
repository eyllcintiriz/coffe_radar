import streamlit as st
import sqlite3

def verification_page():
    st.title("Email Doğrulama")
    token = st.experimental_get_query_params().get('token', [None])[0]
    if token:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM email_verification WHERE token = ?", (token,))
        result = cursor.fetchone()
        if result:
            username = result[0]
            cursor.execute("UPDATE users SET email_verified = 1 WHERE username = ?", (username,))
            cursor.execute("DELETE FROM email_verification WHERE token = ?", (token,))
            conn.commit()
            st.success("Email adresiniz başarıyla doğrulandı!")
        else:
            st.error("Geçersiz veya süresi dolmuş token.")
        conn.close()
    else:
        st.error("Token bulunamadı.")