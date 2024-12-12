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
    #response = requests.get(url, headers=headers, params=params)
    response = {'businesses': [ {
        'name': 'Mock Cafe',
            'location': {'address1': '123 Mock Street', 'display_address': ['123 Mock Street', 'Mock City', 'Mock Country']},
            'coordinates': {
                    'latitude': 40.7128,
                    'longitude': -74.0060
                },
            'rating': 4.5,
    },
    
    ]} # Dummy response for testing
    
    cafes = response.get('businesses', [])

    # response = requests.get(geocode_url, headers=headers)
    response = [{'lat': '0', 'lon': '0'}]  # Mock response for testing

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
                cafes_to_display = cafes[:2]

            for idx, cafe in enumerate(cafes_to_display):
                # Cafe Name
                st.markdown(f"<h4 style='margin-bottom:5px;'>{cafe['name']}</h4>", unsafe_allow_html=True)

                # Compact Cafe Details
                cafe_details = f"{cafe.get('rating', 'N/A')} ⭐ | {', '.join(cafe['location']['display_address'])}"
                st.write(cafe_details)

                user_id = get_user_id(st.session_state["username"])

                # Compact Buttons in a Single Row
                cols = st.columns([1, 1, 1, 4])

                with cols[0]:
                    if not is_cafe_in_favorites(user_id, cafe['name']):
                        if st.button("❤️", key=f"fav_{idx}"):
                            add_favorite_cafe(user_id, cafe['name'])
                            st.success("Added to favorites!")
                    else:
                        st.write("❤️")

                with cols[1]:
                    if st.button("✍️", key=f"review_{idx}"):
                        st.session_state[f"show_review_form_{idx}"] = not st.session_state.get(f"show_review_form_{idx}", False)

                with cols[2]:
                    if st.button("🚩", key=f"report_{idx}"):
                        st.session_state[f"show_report_form_{idx}"] = not st.session_state.get(f"show_report_form_{idx}", False)

                with cols[3]:
                    pass  # Placeholder for alignment

                # Show Review Form if Toggled
                if st.session_state.get(f"show_review_form_{idx}", False):
                    with st.form(key=f"review_form_{idx}"):
                        review_text_input = st.text_area("Your Review", key=f"review_text_{idx}")
                        rating_input = st.slider("Rating", 1, 5, 3, key=f"rating_slider_{idx}")
                        submit_review = st.form_submit_button("Submit")
                        if submit_review:
                            success, message = add_review(user_id, cafe['name'], review_text_input, rating_input)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)

                # Show Report Form if Toggled
                if st.session_state.get(f"show_report_form_{idx}", False):
                    with st.form(key=f"report_form_{idx}"):
                        reason = st.text_area("Reason for reporting", key=f"report_reason_{idx}")
                        submit_report = st.form_submit_button("Submit Report")
                        if submit_report:
                            user_id = get_user_id(st.session_state["username"])
                            add_report(user_id, cafe['name'], reason)
                            st.success("Report submitted successfully.")
                            st.session_state[f"show_report_form_{idx}"] = False

                # Display Reviews Compactly
                reviews = get_reviews(cafe['name'])
                if reviews:
                    st.write(f"✨ Reviews ({len(reviews)}):")
                    for review_text, rating_value, reviewer_username in reviews[:1]:  # Show only first review
                        st.write(f"- {rating_value}⭐ {reviewer_username}: {review_text}")
                else:
                    st.write("No reviews yet.")

                # Divider with reduced margin
                st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)

            # Show More/Less Button
            if not st.session_state['show_all_cafes']:
                if st.button("Show More"):
                    st.session_state['show_all_cafes'] = True
                    st.rerun()
            else:
                if st.button("Show Less"):
                    st.session_state['show_all_cafes'] = False
                    st.rerun()

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