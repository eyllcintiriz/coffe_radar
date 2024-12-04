# favorite_cafes.py
import streamlit as st
from db_helpers import get_user_id, get_favorite_cafes, remove_favorite_cafe
import json

def favorite_cafes_page():
    st.title("Your Favorite Cafes")

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
                    remove_favorite_cafe(user_id, cafe_json['id'])
                    st.success(f"Removed {cafe_json['name']} from favorites!")
                    st.rerun()

            with col2:
                # Cafe image
                st.image(cafe_json.get('image_url', 'https://via.placeholder.com/100'), width=100)

            with col3:
                cafe_name = cafe_json['name']
                if st.button(cafe_name, key=f"fav_cafe_{idx}"):
                    st.session_state['selected_cafe'] = cafe_json
                    st.session_state['page'] = 'Cafe Details'
                    st.rerun()
                st.write(f"Rating: {cafe_json.get('rating', 'N/A')} ⭐ ({cafe_json.get('review_count', 0)} reviews)")
                st.write(f"Address: {', '.join(cafe_json['location']['display_address'])}")
                st.write(f"Phone: {cafe_json.get('display_phone', 'N/A')}")
                st.write("---")
    else:
        st.info("You haven't added any favorite cafes yet.")