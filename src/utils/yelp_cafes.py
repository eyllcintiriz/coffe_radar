import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
import math
from src.utils.db_helpers import get_user_id, is_cafe_in_favorites, add_favorite_cafe, add_report, add_review, calculate_rating, remove_favorite_cafe, add_cafe, get_cafes
import json

API_KEY = 'SrpDGlkbBf5SaTBTk4rBv2HiPdFC4SZwITVQVorbj6cN0g3Z_tB1k1pWPFZqPoUuKu_yX1b7F3-K6uoe-lc6s5Y4iyek4e4oG3HPmi_DyXOmZK-tK3EBBQCvPLJQZ3Yx'

def fetch_cafes(latitude=None, longitude=None, term="cafe"):
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

def display_cafes_on_map(latitude, longitude, location_name="Konumunuz", key_prefix="map_"):
    if len(get_cafes()) > 0:
        cafes = get_cafes()
        st.write(f"{location_name} civarında {len(cafes)} kafe bulundu.")
    else:
        data = fetch_cafes(latitude, longitude)
        if "businesses" in data:
            cafes = data["businesses"]
            for cafe in cafes:
                add_cafe(cafe['name'], cafe['location']['address1'], json.dumps(cafe))
            st.write(f"{location_name} civarında {len(cafes)} kafe bulundu.")
        else:
            cafes = []
            st.error("Kafe bulunamadı.")
            return

    # Include categories
    cafes_df = pd.DataFrame([{
        'name': cafe['name'],
        'lat': cafe['coordinates']['latitude'],
        'lon': cafe['coordinates']['longitude'],
        'distance': cafe.get('distance', 0),
        'rating': cafe.get('rating', 0),
        'review_count': cafe.get('review_count', 0),
        'image_url': cafe.get('image_url', ''),
        'location': cafe.get('location', {}),
        'phone': cafe.get('display_phone', 'N/A'),
        'categories': [cat['title'] for cat in cafe.get('categories', [])]
    } for cafe in cafes])

    # Store cafes_df in session
    st.session_state[f"{key_prefix}cafes_df"] = cafes_df

    sort_option = st.selectbox("Kafeleri sırala:", ["Distance", "Rating", "Popularity"], key=f"sort_{key_prefix}{latitude}_{longitude}")
    cafes_df = sort_cafes_df(cafes_df, sort_option)
    st.session_state[f"{key_prefix}cafes_df"] = cafes_df




    metric = sort_option.lower()
    if metric == "popularity":
        metric = "review_count"

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

    user_df = pd.DataFrame([{
        'name': 'Your Location',
        'lat': latitude,
        'lon': longitude
    }])

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

    display_cafe_list(key_prefix=key_prefix)

def display_cafe_list(key_prefix=None):
    st.subheader("Kafeler")

    # Retrieve cafes_df from session state
    if f"{key_prefix}cafes_df" not in st.session_state:
        st.write("Veri bulunamadı.")
        return

    cafes_df = st.session_state[f"{key_prefix}cafes_df"]

    show_all_key = f'{key_prefix}_show_all'
    if show_all_key not in st.session_state:
        st.session_state[show_all_key] = False

    if st.session_state[show_all_key]:
        cafes_to_display = cafes_df
    else:
        cafes_to_display = cafes_df.head(3)

    for idx, cafe in cafes_to_display.iterrows():
        cafe_dict = cafe.to_dict()  # Convert to dict for easy access
        col1, col2 = st.columns([1, 3])

        with col1:
            if cafe_dict['image_url']:
                st.image(cafe_dict['image_url'], width=200)
            else:
                st.image("https://via.placeholder.com/200", width=200)

        with col2:
            cafe_name = cafe_dict['name']
            if st.button(cafe_name, key=f"{key_prefix}{idx}"):
                st.session_state['selected_cafe'] = cafe_dict
                st.session_state['page'] = 'Kafe Detayları'
                st.rerun()
            rating, review_count = calculate_rating(cafe_dict['rating'], cafe_dict['review_count'], cafe_name)
            st.write(f"Puan: {rating} ⭐ ({review_count} yorum)")

            if 'display_address' in cafe_dict['location']:
                st.write(f"Adres: {', '.join(cafe_dict['location']['display_address'])}")
            else:
                st.write("Adres: N/A")

            st.write(f"Telefon: {cafe_dict['phone']}")
            st.write(f"Kategori(ler): {', '.join(cafe_dict['categories'])}")

            st.markdown("---")

            icon_cols = st.columns(3)
            user_id = get_user_id(st.session_state.get("username", ""))

            with icon_cols[0]:
                if user_id:
                    if is_cafe_in_favorites(user_id, cafe_name):
                        if st.button("❤️", key=f"fav_{key_prefix}_{cafe_name}_{idx}"):
                            remove_favorite_cafe(user_id, cafe_name)
                            st.success(f"{cafe_name} favorilerinizden silindi!")
                            st.rerun()
                    else:
                        if st.button("🤍", key=f"fav_{key_prefix}_{cafe_name}_{idx}"):
                            add_favorite_cafe(user_id, cafe_name, json.dumps(cafe_dict))
                            st.success(f"{cafe_name} favorilerinize eklendi!")
                            st.rerun()

            with icon_cols[1]:
                if st.button("✍️", key=f"review_{key_prefix}_{cafe_name}_{idx}"):
                    st.session_state[f"show_review_form_{key_prefix}_{cafe_name}_{idx}"] = not st.session_state.get(f"show_review_form_{key_prefix}_{cafe_name}_{idx}", False)

            with icon_cols[2]:
                if st.button("🚩", key=f"report_{key_prefix}_{cafe_name}_{idx}"):
                    st.session_state[f"show_report_form_{key_prefix}_{cafe_name}_{idx}"] = not st.session_state.get(f"show_report_form_{key_prefix}_{cafe_name}_{idx}", False)

            if st.session_state.get(f"show_review_form_{key_prefix}_{cafe_name}_{idx}", False):
                with st.form(key=f"review_form_{key_prefix}_{cafe_name}_{idx}"):
                    review_text = st.text_area("Yorumunuz")
                    rat = st.slider("Puan", 1, 5, 3)
                    if st.form_submit_button("Gönder"):
                        success, message = add_review(user_id, cafe_name, review_text, rat)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)

            if st.session_state.get(f"show_report_form_{key_prefix}_{cafe_name}_{idx}", False):
                with st.form(key=f"report_form_{key_prefix}_{cafe_name}_{idx}"):
                    reason = st.text_area("Report reason")
                    if st.form_submit_button("Submit Report"):
                        add_report(user_id, cafe_name, reason)
                        st.success("Report submitted successfully.")
                        st.session_state[f"show_report_form_{key_prefix}_{cafe_name}_{idx}"] = False

    # Show more/less toggle
    if not st.session_state[show_all_key] and len(cafes_df) > 3:
        if st.button("Daha Fazla", key=f"show_more_{key_prefix}"):
            st.session_state[show_all_key] = True
            st.rerun()
    elif st.session_state[show_all_key] and len(cafes_df) > 3:
        if st.button("Daha Az", key=f"show_less_{key_prefix}"):
            st.session_state[show_all_key] = False
            st.rerun()

def sort_cafes_df(cafes_df, sort_option):
    if sort_option == "Distance":
        cafes_df = cafes_df.sort_values(by="distance")
    elif sort_option == "Rating":
        cafes_df = cafes_df.sort_values(by="rating", ascending=False)
    elif sort_option == "Popularity":
        cafes_df = cafes_df.sort_values(by="review_count", ascending=False)
    return cafes_df

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon1 - lon2)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance * 1000  # Return distance in meters
