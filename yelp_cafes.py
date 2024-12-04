# yelp_cafes.py
import streamlit as st
import requests
import pandas as pd
from db_helpers import get_user_id, is_cafe_in_favorites, add_favorite_cafe
import json

API_KEY = 'SrpDGlkbBf5SaTBTk4rBv2HiPdFC4SZwITVQVorbj6cN0g3Z_tB1k1pWPFZqPoUuKu_yX1b7F3-K6uoe-lc6s5Y4iyek4e4oG3HPmi_DyXOmZK-tK3EBBQCvPLJQZ3Yx'

def fetch_cafes(latitude, longitude, term="cafe"):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }
    params = {
        "term": term,
        "latitude": latitude,
        "longitude": longitude,
        "limit": 50
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def display_cafes_on_map(latitude, longitude, location_name="your location"):
    data = fetch_cafes(latitude, longitude)
    if "businesses" in data:
        cafes = data["businesses"]
        st.write(f"Found {len(cafes)} cafes near {location_name}")

        # Create a DataFrame for map display
        df = pd.DataFrame([{
            'name': cafe['name'],
            'lat': cafe['coordinates']['latitude'],
            'lon': cafe['coordinates']['longitude']
        } for cafe in cafes])

        # Display the map
        st.map(df)

        # Display the cafe list below the map
        st.subheader("Cafe List")

        # Handle "Show More" functionality
        if 'show_all_cafes' not in st.session_state:
            st.session_state['show_all_cafes'] = False

        # Determine the cafes to display
        if st.session_state['show_all_cafes']:
            cafes_to_display = cafes
        else:
            cafes_to_display = cafes[:3]

        user_id = get_user_id(st.session_state.get("username", ""))

        # Display the cafes with images and favorite buttons
        for idx, cafe in enumerate(cafes_to_display):
            col1, col2, col3 = st.columns([1, 1, 3])
            serialized_cafe = json.dumps(cafe)
            with col1:
                # Favorite button with icon
                if user_id:
                    if is_cafe_in_favorites(user_id, cafe['id']):
                        st.button("❤️", disabled=True, key=f"fav_{idx}")
                    else:
                        if st.button("🤍", key=f"fav_{idx}"):
                            add_favorite_cafe(user_id, cafe['id'], serialized_cafe)
                            st.success(f"Added {cafe['name']} to favorites!")
                            st.rerun()
                else:
                    st.write("")
  
            with col2:
                if cafe.get('image_url'):
                    st.image(cafe['image_url'], width=100)
                else:
                    st.image("https://via.placeholder.com/100", width=100)

            with col3:
                cafe_name = cafe['name']
                if st.button(cafe_name, key=f"cafe_{idx}"):
                    st.session_state['selected_cafe'] = cafe
                    st.session_state['page'] = 'Cafe Details'
                    st.rerun()
                st.write(f"Rating: {cafe.get('rating', 'N/A')} ⭐ ({cafe.get('review_count', 0)} reviews)")
                st.write(f"Address: {', '.join(cafe['location']['display_address'])}")
                st.write(f"Phone: {cafe.get('display_phone', 'N/A')}")
                st.write("---")
        # Show "Show More" or "Show Less" button
        if not st.session_state['show_all_cafes'] and len(cafes) > 3:
            if st.button("Show More"):
                st.session_state['show_all_cafes'] = True
                st.rerun()
        elif st.session_state['show_all_cafes']:
            if st.button("Show Less"):
                st.session_state['show_all_cafes'] = False
                st.rerun()
    else:
        st.error("No cafes found or an error occurred.")