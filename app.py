# app.py
import streamlit as st
from login_page import login_page
from main_page import main_page
from favorite_cafes import favorite_cafes_page
from register_page import register_page
from profile_1 import profile_page
from cafe_details import cafe_details_page
from feedback_page import feedback_page  # Import the feedback page

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "Ana Sayfa"

# Page navigation
if st.session_state["logged_in"]:
    st.sidebar.title("Sayfalar")

    # Define the pages that should appear in the sidebar
    sidebar_pages = ["Ana Sayfa", "Favori Kafeler", "Profil", "Geri Bildirim Gönderin"]

    # Use a separate variable for the sidebar selection
    sidebar_selection = st.sidebar.radio(
        "Geçiş Yap:",
        options=sidebar_pages,
        index=sidebar_pages.index(st.session_state.get("sidebar_page", "Ana Sayfa")),
        key='sidebar_navigation'
    )

    # Update the sidebar page in session state
    st.session_state["sidebar_page"] = sidebar_selection

    if st.sidebar.button("Çıkış Yap"):
        st.session_state["logged_in"] = False
        st.session_state["page"] = "Ana Sayfa"
        st.experimental_rerun()

    # Only change the main page if the sidebar selection is different and we're not on an internal page
    if st.session_state["page"] in sidebar_pages or st.session_state["page"] == st.session_state.get("previous_page", ""):
        st.session_state["page"] = sidebar_selection

    # Save the previous page
    st.session_state["previous_page"] = st.session_state["page"]

    # Navigate to the selected page
    if st.session_state["page"] == "Ana Sayfa":
        main_page()
    elif st.session_state["page"] == "Favori Kafeler":
        favorite_cafes_page()
    elif st.session_state["page"] == "Profil":
        profile_page()
    elif st.session_state["page"] == "Geri Bildirim Gönderin":
        feedback_page()
    elif st.session_state["page"] == "Cafe Details":
        cafe_details_page()
    else:
        # Default to main page if the page is unrecognized
        main_page()
else:
    # Handle authentication pages
    auth_options = ["Giriş Yap", "Kayıt Ol"]
    default_index = auth_options.index(st.session_state.get("auth_option", "Giriş Yap"))
    auth_option = st.sidebar.radio("Seçiminizi Yapın", auth_options, index=default_index)
    st.session_state["auth_option"] = auth_option
    if auth_option == "Giriş Yap":
        login_page()
    else:
        register_page()
