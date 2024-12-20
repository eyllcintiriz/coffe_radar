import time
import streamlit as st
from src.utils.db_helpers import authenticate

def login_page():
    st.title("Giriş Yap")
    with st.form(key='login_form'):
        username = st.text_input("Kullanıcı Adı")
        password = st.text_input("Şifre", type="password")
        submit_button = st.form_submit_button("Giriş Yap")
    if submit_button:
        user = authenticate(username, password)
        if user or (username == "admin" and password == "admin_password"):  # Check for admin credentials
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            # Initialize tutorial state if not already done
            if "tutorial_completed" not in st.session_state:
                st.session_state["tutorial_completed"] = False

            st.success(f"Merhaba, {username}! Yönlendiriliyorsunuz...")
            time.sleep(1)
            st.rerun()
        else:
            error_placeholder = st.empty()
            error_placeholder.error("Kullanıcı adı veya şifre hatalı!")
            time.sleep(3)
            error_placeholder.empty()
