# cafe_details.py
import time
import streamlit as st
from db_helpers import calculate_rating

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def cafe_details_page():
    cafe = st.session_state.get('selected_cafe', None)
    if cafe is None:
        st.error("No cafe selected.")
        return

    st.title(cafe['name'])

    # Display cafe image
    st.image(cafe.get('image_url', 'https://via.placeholder.com/400'), width=400)

    # Display detailed information
    st.subheader("Details")
    rating, review_count = calculate_rating(cafe.get('rating', 0), cafe.get('review_count', 0), cafe['name'])
    st.write(f"**Rating:** {rating} ⭐ ({review_count} review(s))")
    st.write(f"**Price:** {cafe.get('price', 'N/A')}")
    st.write(f"**Phone:** {cafe.get('display_phone', 'N/A')}")
    st.write(f"**Address:** {', '.join(cafe['location']['display_address'])}")
    st.write(f"**Categories:** {', '.join([category['title'] for category in cafe.get('categories', [])])}")
    
		# Display hours of operation if available
    hours = cafe.get('business_hours', [])
    if hours:
      st.subheader("Hours of Operation")
      for hour in hours[0]['open']:
        
        day_name = DAYS[hour['day']]
        # Format 'start' and 'end' times as HH:MM
        start_time = f"{hour['start'][:2]}:{hour['start'][2:]}"
        end_time = f"{hour['end'][:2]}:{hour['end'][2:]}"
        
        # Display the formatted hours
        st.write(f"**{day_name}**: {start_time} - {end_time}")
              
    # Display additional attributes if available
    attributes = cafe.get('attributes', {})
    if attributes:
      st.subheader("Additional Information")
      for key, value in attributes.items():
          if value is not None:
            if isinstance(value, dict):
                value = ', '.join([f"{k}: {v}" for k, v in value.items()])
            elif isinstance(value, bool):
                value = "✅" if value else "❌"
            st.write(f"**{key.replace('_', ' ').title()}**: {value}")

    # Back button
    if st.button("Back to Cafe List"):
        st.session_state['page'] = st.session_state.get("previous_page", "Ana Sayfa")
        st.rerun()