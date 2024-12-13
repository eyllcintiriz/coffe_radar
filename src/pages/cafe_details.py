import time
import streamlit as st
from src.utils.db_helpers import calculate_rating, get_reviews

DAYS = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']

def cafe_details_page():
    cafe = st.session_state.get('selected_cafe', None)
    if cafe is None:
        st.error("Hiçbir kafe seçilmedi.")
        return

    st.title(cafe['name'])

    # Display cafe image
    st.image(cafe.get('image_url', 'https://via.placeholder.com/400'), width=400)

    # Display detailed information
    st.subheader("Detaylar")
    rating, review_count = calculate_rating(cafe.get('rating', 0), cafe.get('review_count', 0), cafe['name'])
    st.write(f"**Puan:** {rating} ⭐ ({review_count} yorum)")
    st.write(f"**Fiyat:** {cafe.get('price', 'N/A')}")
    st.write(f"**Telefon:** {cafe.get('display_phone', 'N/A')}")
    st.write(f"**Adres:** {', '.join(cafe['location']['display_address'])}")
    
    # Display hours of operation if available
    hours = cafe.get('business_hours', [])
    if hours:
      st.subheader("Açık Olduğu Saatler")
      for hour in hours[0]['open']:
        
        day_name = DAYS[hour['day']]
        # Format 'start' and 'end' times as HH:MM
        start_time = f"{hour['start'][:2]}:{hour['start'][2:]}"
        end_time = f"{hour['end'][:2]}:{hour['end'][2:]}"
        
        # Display the formatted hours
        st.write(f"**{day_name}**: {start_time} - {end_time}")
        
    # Display reviews of the cafe from our users
    reviews = get_reviews(cafe['name'])
    # Display as a table of username, rating, review text
    st.subheader("Kullanıcı Yorumları")
    if not reviews:
      st.info("Henüz hiç yorum yapılmamış.")
    else:
      for review in reviews:
        review_text, rating, username = review
        st.write(f"**{username}** - Puan: {rating} ⭐")
        st.write("Yorum:",review_text)
        st.write("---")
    
              
    # Display additional attributes if available
    attributes = cafe.get('attributes', {})
    if attributes:
      st.subheader("Ek Özellikler")
      for key, value in attributes.items():
          if value is not None:
            if isinstance(value, dict):
                value = ', '.join([f"{k}: {v}" for k, v in value.items()])
            elif isinstance(value, bool):
                value = "✅" if value else "❌"
            st.write(f"**{key.replace('_', ' ').title()}**: {value}")

    # Back button
    if st.button("Kafe Listesine Geri Dön"):
        st.session_state['page'] = st.session_state.get("previous_page", "Ana Sayfa")
        st.rerun()