import streamlit as st
from db_helpers import register_user
from policy_page import privacy_policy_page, terms_of_service_page

def register_page():
    st.title("Kayıt Ol")

    # Provide links to view full policies
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Gizlilik Politikasını Görüntüle"):
            privacy_policy_page()
    with col2:
        if st.button("Kullanım Şartlarını Görüntüle"):
            terms_of_service_page()

    # Registration form
    with st.form("Kayıt Formu"):
        username = st.text_input("Kullanıcı Adı")
        password = st.text_input("Şifre", type="password")
        confirm_password = st.text_input("Şifreyi Onayla", type="password")

        # Policy acceptance checkboxes
        privacy_policy_accepted = st.checkbox("Gizlilik Politikasını okudum ve kabul ediyorum")
        terms_of_service_accepted = st.checkbox("Kullanım Şartlarını okudum ve kabul ediyorum")

        submit_button = st.form_submit_button("Kayıt Ol")

        if submit_button:
            # Validate inputs
            if not username or not password:
                st.error("Kullanıcı adı ve şifre boş bırakılamaz!")
                return

            if password != confirm_password:
                st.error("Şifreler eşleşmiyor!")
                return

            if not privacy_policy_accepted or not terms_of_service_accepted:
                st.error("Kayıt olmak için Gizlilik Politikası ve Kullanım Şartlarını kabul etmelisiniz!")
                return

            # Attempt to register
            success, message = register_user(username, password)
            
            if success:
                st.success(message)
                st.session_state["username"] = username
                st.session_state["logged_in"] = True
                st.session_state["page"] = "Ana Sayfa"
                st.experimental_rerun()
            else:
                st.error(message)
