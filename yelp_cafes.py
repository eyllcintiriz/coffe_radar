# yelp_cafes.py
import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
from db_helpers import get_user_id, is_cafe_in_favorites, add_favorite_cafe, add_report, add_review, get_reviews, calculate_rating
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

        # Create a DataFrame for the map
        df = pd.DataFrame([{
            'name': cafe['name'],
            'lat': cafe['coordinates']['latitude'],
            'lon': cafe['coordinates']['longitude']
        } for cafe in cafes])

        # Use the second version's styling of the map (pydeck)
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=10,  
            radius_min_pixels=10,  
            radius_max_pixels=300,  
            pickable=True,
            auto_highlight=True,
        )

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

        view_state = pdk.ViewState(
            latitude=latitude,
            longitude=longitude,
            zoom=13,
            pitch=50,
        )

        r = pdk.Deck(
            layers=[layer, text_layer],
            initial_view_state=view_state,
            tooltip={"text": "{name}"}
        )

        st.pydeck_chart(r)

        # Display the cafe list below the map (from the first version layout)
        st.subheader("Cafe List")

        # Show More / Show Less handling
        if 'show_all_cafes' not in st.session_state:
            st.session_state['show_all_cafes'] = False

        if st.session_state['show_all_cafes']:
            cafes_to_display = cafes
        else:
            cafes_to_display = cafes[:3]

        user_id = get_user_id(st.session_state.get("username", ""))

        # Display each cafe
        for idx, cafe in enumerate(cafes_to_display):
            col1, col2 = st.columns([1, 3])

            # Convert cafe object to json for adding to favorites
            serialized_cafe = json.dumps(cafe)

            with col1:
                # Keep the cafe photo from the first version
                if cafe.get('image_url'):
                    st.image(cafe['image_url'], width=100)
                else:
                    st.image("https://via.placeholder.com/100", width=100)

            with col2:
                # Cafe name as a button (first version logic)
                cafe_name = cafe['name']
                if st.button(cafe_name, key=f"cafe_{idx}"):
                    st.session_state['selected_cafe'] = cafe
                    st.session_state['page'] = 'Kafe Detayları'
                    st.rerun()
                rating, review_count = calculate_rating(cafe.get('rating', 0), cafe.get('review_count', 0), cafe['name'])
                st.write(f"Rating: {rating} ⭐ ({review_count} review(s))")
                st.write(f"Address: {', '.join(cafe['location']['display_address'])}")
                st.write(f"Phone: {cafe.get('display_phone', 'N/A')}")

                # Add a small divider
                st.markdown("---")

            # Create a new row of columns for the three icons (❤️,✍️,🚩) plus spacing
            icon_cols = col2.columns([1,1,1,4])

            # Favorite button from first version logic but placed in the layout style from second version
            with icon_cols[0]:
                if user_id:
                    if is_cafe_in_favorites(user_id, cafe['id']):
                        st.button("❤️", key=f"fav_{idx}")
                    else:
                        # If not, show a "🤍" button
                        if st.button("🤍", key=f"fav_{idx}"):
                            add_favorite_cafe(user_id, cafe['id'], serialized_cafe)
                            st.success(f"Added {cafe['name']} to favorites!")
                            st.rerun()
                else:
                    # If no user_id, just leave blank or prompt login
                    st.write("")

            # Review button (✍️) from second version logic
            with icon_cols[1]:
                if st.button("✍️", key=f"review_{idx}"):
                    st.session_state[f"show_review_form_{idx}"] = not st.session_state.get(f"show_review_form_{idx}", False)

            # Report button (🚩) from second version logic
            with icon_cols[2]:
                if st.button("🚩", key=f"report_{idx}"):
                    st.session_state[f"show_report_form_{idx}"] = not st.session_state.get(f"show_report_form_{idx}", False)

            # Align the buttons row
            # icon_cols[3] is just a spacer, do nothing
            with icon_cols[3]:
                pass

            # Show Review Form if toggled
            if st.session_state.get(f"show_review_form_{idx}", False):
                with st.form(key=f"review_form_{idx}"):
                    review_text_input = st.text_area("Your Review", key=f"review_text_{idx}")
                    rating_input = st.slider("Rating", 1, 5, 3, key=f"rating_slider_{idx}")
                    submit_review = st.form_submit_button("Submit")
                    if submit_review:
                        success, message = add_review(user_id, cafe_name, review_text_input, rating_input)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

            # Show Report Form if toggled
            if st.session_state.get(f"show_report_form_{idx}", False):
                with st.form(key=f"report_form_{idx}"):
                    reason = st.text_area("Reason for reporting", key=f"report_reason_{idx}")
                    submit_report = st.form_submit_button("Submit Report")
                    if submit_report:
                        add_report(user_id, cafe_name, reason)
                        st.success("Report submitted successfully.")
                        st.session_state[f"show_report_form_{idx}"] = False

            # Display a compact view of reviews from second version logic (just show the first review)
            reviews = get_reviews(cafe_name)
            if reviews:
                st.write(f"✨ Reviews ({len(reviews)}):")
                # Show only the first review
                first_review_text, first_review_rating, first_review_user = reviews[0]
                st.write(f"- {first_review_rating}⭐ {first_review_user}: {first_review_text}")
            else:
                st.write("No reviews yet.")

            st.markdown("<hr style='margin:10px 0;'>", unsafe_allow_html=True)

        # Show More / Show Less buttons
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