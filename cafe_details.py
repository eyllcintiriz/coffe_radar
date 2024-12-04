# cafe_details.py
import streamlit as st
from db_helpers import get_user_id, is_cafe_in_favorites, add_favorite_cafe, remove_favorite_cafe

def cafe_details_page():
    cafe = st.session_state.get('selected_cafe', None)
    if cafe is None:
        st.error("No cafe selected.")
        return

    st.title(cafe['name'])

    user_id = get_user_id(st.session_state.get("username", ""))

    # Display cafe image
    st.image(cafe.get('image_url', 'https://via.placeholder.com/400'), width=400)

    # Favorite or unfavorite button
    if user_id:
        if is_cafe_in_favorites(user_id, cafe['id']):
            if st.button("Remove from Favorites ❤️"):
                remove_favorite_cafe(user_id, cafe['id'])
                st.success(f"Removed {cafe['name']} from favorites!")
                st.rerun()
        else:
            if st.button("Add to Favorites 🤍"):
                add_favorite_cafe(user_id, cafe['id'], cafe)
                st.success(f"Added {cafe['name']} to favorites!")
                st.rerun()

    # Display detailed information
    st.subheader("Details")
    st.write(f"**Rating:** {cafe.get('rating', 'N/A')} ⭐ ({cafe.get('review_count', 0)} reviews)")
    st.write(f"**Price:** {cafe.get('price', 'N/A')}")
    st.write(f"**Phone:** {cafe.get('display_phone', 'N/A')}")
    st.write(f"**Address:** {', '.join(cafe['location']['display_address'])}")
    st.write(f"**Categories:** {', '.join([category['title'] for category in cafe.get('categories', [])])}")
    
		# Display hours of operation if available - Doğru çalışmıyor
    hours = cafe.get('hours', [])
    if hours:
      st.subheader("Hours of Operation")
      for hour in hours[0]['open']:
        st.write(f"**{hour['day']}**: {hour['start']} - {hour['end']}")
    else:
      st.write("Hours of operation not available.")
              
    # Display additional attributes if available
    attributes = cafe.get('attributes', {})
    if attributes:
        st.subheader("Additional Information")
        for key, value in attributes.items():
            if value is not None:
                if isinstance(value, dict):
                    value = ', '.join([f"{k}: {v}" for k, v in value.items()])
                st.write(f"**{key.replace('_', ' ').title()}**: {value}")

    # Link to Yelp page
    if cafe.get('url'):
        st.markdown(f"[View on Yelp]({cafe['url']})")

    # Back button
    if st.button("Back to Cafe List"):
        st.session_state['page'] = st.session_state.get("previous_page", "Ana Sayfa")
        st.rerun()