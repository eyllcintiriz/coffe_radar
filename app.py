import streamlit as st
from login_page import login_page
from main_page import main_page
from favorite_cafes import favorite_cafes_page
from register_page import register_page
from profile_1 import profile_page

# Oturum durumu
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "Ana Sayfa"

# Sidebar sayfa geçişleri
if st.session_state["logged_in"]:
    st.sidebar.title("Sayfalar")
    page = st.sidebar.radio(
        "Geçiş Yap:",
        options=["Ana Sayfa", "Favori Kafeler", "Profil"],
        index=["Ana Sayfa", "Favori Kafeler", "Profil"].index(st.session_state["page"]),
    )
    st.session_state["page"] = page

    if st.sidebar.button("Çıkış Yap"):
        st.session_state["logged_in"] = False
        st.session_state["page"] = "Ana Sayfa"
        st.rerun()  # UI'yı güncellemek için yeniden çalıştır

    # Seçime göre sayfa çağırma
    if st.session_state["page"] == "Ana Sayfa":
        main_page()
    elif st.session_state["page"] == "Favori Kafeler":
        favorite_cafes_page()
    elif st.session_state["page"] == "Profil":
        profile_page()
else:
    auth_options = ["Giriş Yap", "Kayıt Ol"]
    default_index = auth_options.index(st.session_state.get("auth_option", "Giriş Yap"))
    auth_option = st.sidebar.radio("Seçiminizi Yapın", auth_options, index=default_index)
    st.session_state["auth_option"] = auth_option
    if auth_option == "Giriş Yap":
        login_page()
    else:
        register_page()