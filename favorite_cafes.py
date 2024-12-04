import streamlit as st
import time
from db_helpers import get_user_id, get_favorite_cafes, remove_favorite_cafe

# Favori kafeler sayfası
def favorite_cafes_page():
    st.title("Favori Kafeleriniz")
    
    user_id = get_user_id(st.session_state["username"])
    cafes = get_favorite_cafes(user_id)
    
    if cafes:
        for cafe in cafes:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(cafe)
            with col2:
                if st.button(f"Favorilerden Çıkar: {cafe}", key=f"remove_{cafe}"):
                    remove_favorite_cafe(user_id, cafe)
                    st.success(f"{cafe} favorilerden çıkarıldı!")
                    time.sleep(2)
                    st.rerun()
    else:
        st.info("Henüz favori kafe eklemediniz.")