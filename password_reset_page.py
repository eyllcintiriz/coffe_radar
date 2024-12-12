import streamlit as st
import sqlite3

def reset_password_page():
    st.title("Şifre Sıfırlama")
    token = st.experimental_get_query_params().get('token', [None])[0]
    if token:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM password_reset WHERE token = ?", (token,))
        result = cursor.fetchone()
        if result:
            username = result[0]
            new_password = st.text_input("Yeni Şifre", type="password")
            confirm_password = st.text_input("Yeni Şifreyi Onayla", type="password")
            if st.button("Şifreyi Sıfırla"):
                if new_password == confirm_password:
                    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
                    cursor.execute("DELETE FROM password_reset WHERE token = ?", (token,))
                    conn.commit()
                    st.success("Şifreniz başarıyla sıfırlandı!")
                else:
                    st.error("Şifreler eşleşmiyor!")
            conn.close()
        else:
            st.error("Geçersiz veya süresi dolmuş token.")
    else:
        st.error("Token bulunamadı.")