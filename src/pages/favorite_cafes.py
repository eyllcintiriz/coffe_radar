import time
import streamlit as st
from src.utils.db_helpers import get_user_id, get_favorite_cafes, remove_favorite_cafe
import json

def favorite_cafes_page():
    st.title("Favori Kafeleriniz")

    user_id = get_user_id(st.session_state["username"])
    cafes = get_favorite_cafes(user_id)
    
    if cafes:
        # Display the cafes with images and remove buttons
        for idx, cafe in enumerate(cafes):
            col1, col2, col3 = st.columns([1, 1, 3])
            cafe_json = json.loads(cafe[3])
            with col1:
                # Remove favorite button with icon
                if st.button("🗑️", key=f"remove_{idx}"):
                    remove_favorite_cafe(user_id, cafe_json.get('id', cafe[2]))  # Use integer index to access tuple element
                    st.success(f"{cafe_json['name']} favorilerden kaldırıldı!")
                    time.sleep(2)
                    st.rerun()

            with col2:
                # Cafe image
                if cafe_json.get('image_url'):
                    st.image(cafe_json['image_url'], width=200)
                else:
                    st.image("https://via.placeholder.com/200", width=200)

            with col3:
                cafe_name = cafe_json['name']
                if st.button(cafe_name, key=f"fav_cafe_{idx}"):
                    st.session_state['selected_cafe'] = cafe_json
                    st.session_state['page'] = 'Kafe Detayları'
                    st.rerun()
                st.write(f"Puan: {cafe_json.get('rating', 'N/A')} ⭐ ({cafe_json.get('review_count', 0)} yorum)")
                if 'location' in cafe_json and 'display_address' in cafe_json['location']:
                    st.write(f"Adres: {', '.join(cafe_json['location']['display_address'])}")
                else:
                    st.write("Adres: N/A")
                st.write(f"Telefon: {cafe_json.get('display_phone', 'N/A')}")
                st.write("---")
    else:
        st.info("Hiçbir favori kafe eklememişsiniz.")