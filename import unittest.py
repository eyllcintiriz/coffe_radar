import unittest
from unittest.mock import patch
import streamlit as st
from app import main_page, favorite_cafes_page, login_page, register_page

# FILE: test_app.py


class TestApp(unittest.TestCase):

    def setUp(self):
        # Reset session state before each test
        st.session_state.clear()

    @patch('streamlit.sidebar.radio')
    @patch('streamlit.sidebar.button')
    def test_initial_state(self, mock_button, mock_radio):
        # Test initial session state
        self.assertFalse(st.session_state.get("logged_in", False))
        self.assertEqual(st.session_state.get("page", "Ana Sayfa"), "Ana Sayfa")

    @patch('streamlit.sidebar.radio')
    @patch('streamlit.sidebar.button')
    def test_sidebar_page_transitions(self, mock_button, mock_radio):
        # Simulate user logged in
        st.session_state["logged_in"] = True
        st.session_state["page"] = "Ana Sayfa"

        # Simulate sidebar radio button selection
        mock_radio.return_value = "Favori Kafeler"
        mock_button.return_value = False

        # Call the app function to trigger sidebar logic
        main_page()

        # Check if the page transitioned correctly
        self.assertEqual(st.session_state["page"], "Favori Kafeler")

    @patch('streamlit.sidebar.radio')
    @patch('streamlit.sidebar.button')
    def test_login_logout_functionality(self, mock_button, mock_radio):
        # Simulate user logged in
        st.session_state["logged_in"] = True
        st.session_state["page"] = "Ana Sayfa"

        # Simulate logout button click
        mock_button.return_value = True

        # Call the app function to trigger logout logic
        main_page()

        # Check if the user is logged out and page reset
        self.assertFalse(st.session_state["logged_in"])
        self.assertEqual(st.session_state["page"], "Ana Sayfa")

    @patch('streamlit.sidebar.radio')
    @patch('streamlit.sidebar.button')
    def test_page_rendering_based_on_session_state(self, mock_button, mock_radio):
        # Simulate user not logged in
        st.session_state["logged_in"] = False

        # Simulate sidebar radio button selection for auth options
        mock_radio.return_value = "Giriş Yap"
        mock_button.return_value = False

        # Call the app function to trigger page rendering logic
        login_page()

        # Check if the login page is rendered
        self.assertEqual(st.session_state["auth_option"], "Giriş Yap")

if __name__ == '__main__':
    unittest.main()