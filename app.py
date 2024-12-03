import streamlit as st
from login_page import login_page
from main_page import main_page
from favorite_cafes import favorite_cafes_page

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

    # Seçime göre sayfa çağırma
    if st.session_state["page"] == "Ana Sayfa":
        main_page()
    elif st.session_state["page"] == "Favori Kafeler":
        favorite_cafes_page()

else:
    login_page()
