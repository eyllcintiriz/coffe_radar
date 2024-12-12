# yelp_cafes.py
import time
import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
import math
from db_helpers import get_user_id, is_cafe_in_favorites, add_favorite_cafe, add_report, add_review, get_reviews, calculate_rating
from db_helpers import get_user_id, get_cafes, add_cafe, is_cafe_in_favorites, add_favorite_cafe, add_report, add_review, get_reviews, calculate_rating, remove_favorite_cafe
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
    response = requests.get(url, headers=headers, params=params).json()
    return response

def display_cafes_on_map(latitude, longitude, location_name="your location"):
    data = fetch_cafes(latitude, longitude)

    if "businesses" not in data or not data["businesses"]:
        st.error("No cafes found or an error occurred.")
        return

    cafes = data["businesses"]
    st.write(f"Found {len(cafes)} cafes near {location_name}")

    # Create a DataFrame for cafes
    cafes_df = pd.DataFrame([{
        'name': cafe['name'],
        'lat': cafe['coordinates']['latitude'],
        'lon': cafe['coordinates']['longitude'],
        'distance': cafe.get('distance', 0),
        'rating': cafe.get('rating', 0),
        'review_count': cafe.get('review_count', 0),
        'image_url': cafe.get('image_url', ''),
        'location': cafe.get('location', {}),
        'phone': cafe.get('display_phone', 'N/A'),  # Add 'phone' field
    } for cafe in cafes])

    # Sorting options with a unique key
    sort_option = st.selectbox("Sort cafes by:", ["Distance", "Rating", "Popularity"], key=f"sort_{latitude}_{longitude}")
    if sort_option == "Distance":
        cafes_df = cafes_df.sort_values(by="distance")
    elif sort_option == "Rating":
        cafes_df = cafes_df.sort_values(by="rating", ascending=False)
    elif sort_option == "Popularity":
        cafes_df = cafes_df.sort_values(by="review_count", ascending=False)

    # Normalize metric values for color mapping
    metric = sort_option.lower()
    if metric == "popularity":
        metric = "review_count"  # Use review_count as a proxy for popularity

    min_metric = cafes_df[metric].min()
    max_metric = cafes_df[metric].max()
    range_metric = max_metric - min_metric if max_metric != min_metric else 1

    def map_color(value):
        normalized = int(255 * (value - min_metric) / range_metric)
        if metric == 'distance':
            return [normalized, 255 - normalized, 0, 160]
        elif metric == 'rating':
            return [255 - normalized, normalized, 0, 160]
        elif metric == 'review_count':
            return [0, normalized, 255 - normalized, 160]

    cafes_df['color'] = cafes_df[metric].apply(map_color)

    # User location layer
    user_df = pd.DataFrame([{
        'name': 'Your Location',
        'lat': latitude,
        'lon': longitude
    }])

    # Layers for map
    cafes_layer = pdk.Layer(
        'ScatterplotLayer',
        data=cafes_df,
        get_position='[lon, lat]',
        get_fill_color='color',
        get_radius=10,
        radius_min_pixels=10,
        radius_max_pixels=100,
        pickable=True,
        auto_highlight=True,
    )

    user_layer = pdk.Layer(
        'ScatterplotLayer',
        data=user_df,
        get_position='[lon, lat]',
        get_fill_color='[0, 0, 255, 200]',
        get_radius=10,
        radius_min_pixels=10,
        radius_max_pixels=100,
        pickable=False,
    )

    view_state = pdk.ViewState(
        latitude=latitude,
        longitude=longitude,
        zoom=13,
        pitch=50,
    )

    # Render the map
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v9',
        initial_view_state=view_state,
        layers=[cafes_layer, user_layer],
        tooltip={
            'html': '<b>{name}</b><br>Rating: {rating} ⭐',
            'style': {
                'color': 'white'
            }
        }
    ))

    # Display cafe list
    st.subheader("Cafe List")

    if 'show_all_cafes' not in st.session_state:
        st.session_state['show_all_cafes'] = False

    cafes_to_display = cafes_df if st.session_state['show_all_cafes'] else cafes_df.head(3)

    for idx, cafe in cafes_to_display.iterrows():
        col1, col2 = st.columns([1, 3])

        with col1:
            if cafe.get('image_url'):
                st.image(cafe['image_url'], width=200)
            else:
                st.image("https://via.placeholder.com/200", width=200)

        with col2:
            # Cafe name as a button (first version logic)
            cafe_name = cafe['name']
            if st.button(cafe_name, key=f"cafe_{idx}"):
                st.session_state['selected_cafe'] = cafe
                st.session_state['page'] = 'Kafe Detayları'
                st.rerun()
            rating, review_count = calculate_rating(cafe.get('rating', 0), cafe.get('review_count', 0), cafe['name'])
            st.write(f"Rating: {rating} ⭐ ({review_count} review(s))")
            if 'display_address' in cafe['location']:
                st.write(f"Address: {', '.join(cafe['location']['display_address'])}")
            else:
                st.write("Address: N/A")
            st.write(f"Phone: {cafe.get('phone', 'N/A')}")
            st.write(f"Categories: {', '.join(cafe.get('categories', []))}")

            # Add a small divider
            st.markdown("---")


            # Favorite, Review, Report buttons
            icon_cols = st.columns(3)
            user_id = get_user_id(st.session_state.get("username", ""))

            with icon_cols[0]:
                if user_id:
                    if is_cafe_in_favorites(user_id, cafe['name']):
                        if st.button("❤️", key=f"fav_{cafe['name']}_{idx}"):
                            remove_favorite_cafe(user_id, cafe['name'])
                            st.success(f"Removed {cafe['name']} from favorites!")
                            st.rerun()
                    else:
                        if st.button("🤍", key=f"fav_{cafe['name']}_{idx}"):
                            add_favorite_cafe(user_id, cafe['name'], json.dumps(cafe.to_dict()))
                            st.success(f"Added {cafe['name']} to favorites!")
                            st.rerun()

            with icon_cols[1]:
                if st.button("✍️", key=f"review_{cafe['name']}_{idx}"):
                    st.session_state[f"show_review_form_{cafe['name']}_{idx}"] = not st.session_state.get(f"show_review_form_{cafe['name']}_{idx}", False)

            with icon_cols[2]:
                if st.button("🚩", key=f"report_{cafe['name']}_{idx}"):
                    st.session_state[f"show_report_form_{cafe['name']}_{idx}"] = not st.session_state.get(f"show_report_form_{cafe['name']}_{idx}", False)

            if st.session_state.get(f"show_review_form_{cafe['name']}_{idx}", False):
                with st.form(key=f"review_form_{cafe['name']}_{idx}"):
                    review_text = st.text_area("Your Review")
                    rating = st.slider("Rating", 1, 5, 3)
                    if st.form_submit_button("Submit"):
                        success, message = add_review(user_id, cafe['name'], review_text, rating)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

            if st.session_state.get(f"show_report_form_{cafe['name']}_{idx}", False):
                with st.form(key=f"report_form_{cafe['name']}_{idx}"):
                    reason = st.text_area("Reason for reporting")
                    if st.form_submit_button("Submit Report"):
                        add_report(user_id, cafe['name'], reason)
                        st.success("Report submitted successfully.")
                        st.session_state[f"show_report_form_{cafe['name']}_{idx}"] = False

    # Show more/less toggle
    if not st.session_state['show_all_cafes'] and len(cafes_df) > 3:
        if st.button("Show More", key=f"show_more_{location_name}"):
            st.session_state['show_all_cafes'] = True
            st.rerun()
    elif st.session_state['show_all_cafes']:
        if st.button("Show Less", key=f"show_less_{location_name}"):
            st.session_state['show_all_cafes'] = False
            st.rerun()


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon1 - lon2)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance * 1000  # Return distance in meters
