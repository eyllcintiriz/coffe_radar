# filepath: /c:/Users/musta/Documents/GitHub/coffe_radar/recommend_cafe_page.py

import streamlit as st
from db_helpers import get_user_id, submit_recommended_cafe

def recommend_cafe_page():
    st.title("Recommend a Cafe")

    user_id = get_user_id(st.session_state["username"])

    with st.form("recommend_cafe_form"):
        cafe_name = st.text_input("Cafe Name")
        location = st.text_input("Location")
        description = st.text_area("Description")
        submitted = st.form_submit_button("Submit Recommendation")

    if submitted:
        if cafe_name and location:
            submit_recommended_cafe(user_id, cafe_name, location, description)
            st.success("Thank you for your recommendation! It will be reviewed by an admin.")
        else:
            st.error("Please fill in the Cafe Name and Location.")