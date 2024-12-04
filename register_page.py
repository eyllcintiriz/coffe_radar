import streamlit as st
import time
from db_helpers import register_user

def register_page():
    st.title("Kayıt Ol")
    with st.form(key='register_form'):
        username = st.text_input("Kullanıcı Adı")
        password = st.text_input("Şifre", type="password")
        confirm_password = st.text_input("Şifreyi Onayla", type="password")
        submit_button = st.form_submit_button("Kayıt Ol")
    if submit_button:
        if password != confirm_password:
            st.error("Şifreler eşleşmiyor!")
        elif not username or not password:
            st.error("Kullanıcı adı ve şifre gerekli!")
        else:
            success, message = register_user(username, password)
            if success:
                # Mesajları göstermek için bir placeholder oluşturuyoruz
                placeholder = st.empty()
                for i in range(3, 0, -1):
                    placeholder.success(f"Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz ({i})")
                    time.sleep(1)
                placeholder.empty()
                # Otomatik olarak giriş sayfasına yönlendirme
                st.session_state["auth_option"] = "Giriş Yap"
                st.rerun()
            else:
                st.error(message)