# yelp_cafes.py
import streamlit as st
import requests
import pandas as pd
from db_helpers import add_favorite_cafe, add_report, add_review, get_reviews, get_user_id, is_cafe_in_favorites
import pydeck as pdk

API_KEY = 'lhNZ6Ql2yP9UW4bq2u0s1lhSgtZEQ3QDJ4hdAHNlYbox9G-UFg21QWdZ27Jw6c5vmrKbMpx0EnyLNg5oCrccfDEybOYh-c_Jpp2CNq3qUfw103WYqdW5egTtH3VQZ3Yx'

import sqlite3

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
    


    cafes = response.json().get("businesses", [])

    # Store fetched cafes in the database
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    for cafe in cafes:
        try:
            cursor.execute("INSERT INTO cafes (name, location, features) VALUES (?, ?, ?)", 
                           (cafe['name'], ', '.join(cafe['location']['display_address']), ''))
        except sqlite3.IntegrityError:
            pass  # Ignore if the cafe already exists
    conn.commit()
    conn.close()

    return cafes

def display_cafes_on_map(latitude, longitude, location_name="your location"):
    cafes = fetch_cafes(latitude, longitude)
    if cafes:
        st.write(f"Found {len(cafes)} cafes near {location_name}")

        df = pd.DataFrame([{
            'name': cafe['name'],
            'lat': cafe['coordinates']['latitude'],
            'lon': cafe['coordinates']['longitude']
        } for cafe in cafes])

        col1, col2 = st.columns([4, 3])

        with col2:
            st.subheader("Cafe List")

            if 'show_all_cafes' not in st.session_state:
                st.session_state['show_all_cafes'] = False

            if st.session_state['show_all_cafes']:
                cafes_to_display = cafes
            else:
                cafes_to_display = cafes[:3]

            for cafe in cafes_to_display:
                st.markdown(f"**{cafe['name']}**")
                st.write(f"Rating: {cafe.get('rating', 'N/A')} ⭐")
                st.write(f"Address: {', '.join(cafe['location']['display_address'])}")

                user_id = get_user_id(st.session_state["username"])
                if not is_cafe_in_favorites(user_id, cafe['name']):
                    if st.button(f"Add to Favorites: {cafe['name']}", key=f"add_{cafe['name']}"):
                        add_favorite_cafe(user_id, cafe['name'])
                        st.success(f"{cafe['name']} added to favorites!")
                else:
                    st.caption("Already in favorites")
                
                st.write("---")

                # Review Section
                st.subheader("Reviews")
                reviews = get_reviews(cafe['name'])
                for review, rating, username in reviews:
                    st.write(f"**{username}**")
                    st.write(f"Rating: {rating} ⭐")
                    st.write(f"Review: {review}")
                    if st.button(f"Report Review by {username}", key=f"report_review_{username}_{cafe['name']}"):
                        reason = st.text_area("Reason for reporting", key=f"reason_{username}_{cafe['name']}")
                        if st.button(f"Submit Report: {username}", key=f"submit_report_{username}_{cafe['name']}"):
                            add_report(user_id, "review", review_id, reason)
                            st.success("Report submitted!")
                            st.rerun()
                    st.write("---")

                st.subheader("Write a Review")
                review_text = st.text_area("Your Review", key=f"review_{cafe['name']}")
                rating = st.slider("Rating", 1, 5, key=f"rating_{cafe['name']}")
                if st.button(f"Submit Review: {cafe['name']}", key=f"submit_{cafe['name']}"):
                    success, message = add_review(user_id, cafe['name'], review_text, rating)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

                if st.button(f"Report Cafe: {cafe['name']}", key=f"report_cafe_{cafe['name']}"):
                    reason = st.text_area("Reason for reporting", key=f"reason_cafe_{cafe['name']}")
                    if st.button(f"Submit Report: {cafe['name']}", key=f"submit_report_cafe_{cafe['name']}"):
                        add_report(user_id, "cafe", cafe_id, reason)
                        st.success("Report submitted!")
                        st.rerun()

            if not st.session_state['show_all_cafes']:
                if st.button("Show More"):
                    st.session_state['show_all_cafes'] = True
            else:
                if st.button("Show Less"):
                    st.session_state['show_all_cafes'] = False

        with col1:
            # Create a layer to display the cafes
            layer = pdk.Layer(
                'ScatterplotLayer',
                data=df,
                get_position='[lon, lat]',
                get_color='[200, 30, 0, 160]',
                get_radius=10,  # Base radius for bubbles
                radius_min_pixels=10,  # Minimum radius in pixels
                radius_max_pixels=300,  # Maximum radius in pixels
                pickable=True,
                auto_highlight=True,
            )

            # Create a text layer to display the cafe names
            text_layer = pdk.Layer(
                "TextLayer",
                data=df,
                get_position='[lon, lat]',
                get_text='name',
                get_size=20,
                get_color=[0, 0, 0],
                get_angle=0,
                get_text_anchor='middle',
                get_alignment_baseline='center'
            )

            # Set the viewport location
            view_state = pdk.ViewState(
                latitude=latitude,
                longitude=longitude,
                zoom=13,
                pitch=50,
            )

            # Render the map
            r = pdk.Deck(
                layers=[layer, text_layer],
                initial_view_state=view_state,
                tooltip={"text": "{name}"}
            )

            st.pydeck_chart(r)
    else:
        st.error("No cafes found or an error occurred.")