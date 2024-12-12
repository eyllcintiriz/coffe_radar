import time
import streamlit as st
from db_helpers import authenticate

def login_page():
    st.title("Giriş Yap")
    with st.form(key='login_form'):
        username = st.text_input("Kullanıcı Adı")
        password = st.text_input("Şifre", type="password")
        submit_button = st.form_submit_button("Giriş Yap")
    st.write("[Şifremi Unuttum](http://yourdomain.com/forgot_password)")
    if submit_button:
        user = authenticate(username, password)
        if user:
            if user[4]:  # Assuming email_verified is at index 4
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success(f"Merhaba, {username}! Yönlendiriliyorsunuz...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Lütfen email adresinizi doğrulayın.")
        else:
            st.error("Kullanıcı adı veya şifre hatalı!")