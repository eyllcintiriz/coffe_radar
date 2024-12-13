# feedback_page.py
import streamlit as st
from src.utils.db_helpers import get_user_id, submit_feedback

def feedback_page():
    st.title("Geri Bildirim Gönderin")

    user_id = get_user_id(st.session_state["username"])

    st.write("Lütfen geri bildiriminizi aşağıya yazınız:")

    feedback_text = st.text_area("Geri Bildirim", "", height=200)

    if st.button("Gönder"):
        if feedback_text.strip() == "":
            st.warning("Lütfen geri bildirim metni giriniz.")
        else:
            submit_feedback(user_id, feedback_text)
            st.success("Geri bildiriminiz başarıyla gönderildi. Teşekkür ederiz!")
