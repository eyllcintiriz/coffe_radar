# yelp_cafes.py
import streamlit as st
import requests
import pandas as pd

API_KEY = 'lhNZ6Ql2yP9UW4bq2u0s1lhSgtZEQ3QDJ4hdAHNlYbox9G-UFg21QWdZ27Jw6c5vmrKbMpx0EnyLNg5oCrccfDEybOYh-c_Jpp2CNq3qUfw103WYqdW5egTtH3VQZ3Yx'

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

        # Use columns to display map and cafe list side by side
        col1, col2 = st.columns(2)

        with col1:
            st.map(df)

        with col2:
            st.subheader("Cafe List")

            # Handle "Show More" functionality
            if 'show_all_cafes' not in st.session_state:
                st.session_state['show_all_cafes'] = False

            # Determine the cafes to display
            if st.session_state['show_all_cafes']:
                cafes_to_display = cafes
            else:
                cafes_to_display = cafes[:3]

            # Arrange cafes in grid layout
            num_cols = 3  # Number of columns in the grid
            for i in range(0, len(cafes_to_display), num_cols):
                cols = st.columns(num_cols)
                for idx, cafe in enumerate(cafes_to_display[i:i+num_cols]):
                    with cols[idx]:
                        st.markdown(f"**{cafe['name']}**")
                        st.write(f"Rating: {cafe.get('rating', 'N/A')} ⭐")
                        st.write(f"Address: {', '.join(cafe['location']['display_address'])}")
                        st.write("---")

            # Show "Show More" or "Show Less" button
            if not st.session_state['show_all_cafes']:
                if st.button("Show More"):
                    st.session_state['show_all_cafes'] = True
            else:
                if st.button("Show Less"):
                    st.session_state['show_all_cafes'] = False
    else:
        st.error("No cafes found or an error occurred.")