# main_page.py
import streamlit as st
import requests
import geocoder
from yelp_cafes import display_cafes_on_map

def main_page():
    st.title("Cafes Near You")

    # IP-based geolocation
    g = geocoder.ip('me')
    if g.ok and g.latlng:
        latitude, longitude = g.latlng
        display_cafes_on_map(latitude, longitude)
    else:
        st.error("Unable to determine your location via IP address.")

    # User can still search for another location
    st.subheader("Search for another location")
    location = st.text_input("Enter a location", "", key='location_input')
    if st.button("Search", key='search_button'):
        # Use geocoding to get latitude and longitude from location
        geocode_url = f"https://nominatim.openstreetmap.org/search?format=json&q={location}"
        headers = {'User-Agent': 'CoffeeRadar/1.0 (your_email@example.com)'}
        response = requests.get(geocode_url, headers=headers)
        if response.status_code == 200:
            geocode_data = response.json()
            if geocode_data:
                latitude = float(geocode_data[0]['lat'])
                longitude = float(geocode_data[0]['lon'])
                display_cafes_on_map(latitude, longitude, location_name=location)
            else:
                st.error("Location not found.")
        else:
            st.error(f"Error fetching data: {response.status_code}")
