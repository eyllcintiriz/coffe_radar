import streamlit as st
from src.utils.db_helpers import get_user_id, submit_recommended_cafe

def recommend_cafe_page():
    st.title("Kafe Önerin")

    user_id = get_user_id(st.session_state["username"])

    with st.form("recommend_cafe_form"):
        cafe_name = st.text_input("Kafe Adı")
        location = st.text_input("Konum")
        description = st.text_area("Açıklama")
        submitted = st.form_submit_button("Öneriyi Gönder")

    if submitted:
        if cafe_name and location:
            submit_recommended_cafe(user_id, cafe_name, location, description)
            st.success("Öneriniz için teşekkür ederiz. Yönetici onayından sonra yayınlanacaktır.")
        else:
            st.error("Lütfen gerekli alanları doldurun.")