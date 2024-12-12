import streamlit as st
from login_page import login_page
from main_page import main_page
from favorite_cafes import favorite_cafes_page
from register_page import register_page
from admin_page import admin_page
from policy_page import privacy_policy_page, terms_of_service_page

# set the page config to wide
st.set_page_config(layout="wide")

# Oturum durumu
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "Ana Sayfa"

# Sidebar sayfa geçişleri
if st.session_state["logged_in"]:
    st.sidebar.title("Sayfalar")
    page_options = [
        "Ana Sayfa", 
        "Favori Kafeler", 
        "Gizlilik Politikası", 
        "Kullanım Şartları"
    ]
    if st.session_state["username"] == "admin":  # Check for admin user
        page_options.append("Admin Interface")
    page = st.sidebar.radio("Geçiş Yap:", options=page_options)
    st.session_state["page"] = page

    if st.sidebar.button("Çıkış Yap"):
        st.session_state["logged_in"] = False
        st.session_state["page"] = "Ana Sayfa"
        st.rerun()

    if st.session_state["page"] == "Ana Sayfa":
        main_page()
    elif st.session_state["page"] == "Favori Kafeler":
        favorite_cafes_page()
    elif st.session_state["page"] == "Gizlilik Politikası":
        privacy_policy_page()
    elif st.session_state["page"] == "Kullanım Şartları":
        terms_of_service_page()
    elif st.session_state["page"] == "Admin Interface":
        admin_page()
else:
    st.sidebar.title("Yasal Bilgiler")
    legal_options = [
        "Giriş Yap", 
        "Kayıt Ol", 
        "Gizlilik Politikası", 
        "Kullanım Şartları"
    ]
    default_index = legal_options.index(st.session_state.get("legal_option", "Giriş Yap"))
    legal_option = st.sidebar.radio("Seçiminizi Yapın", legal_options, index=default_index)
    st.session_state["legal_option"] = legal_option

    if legal_option == "Giriş Yap":
        login_page()
    elif legal_option == "Kayıt Ol":
        register_page()
    elif legal_option == "Gizlilik Politikası":
        privacy_policy_page()
    else:
        terms_of_service_page()
