import streamlit as st
import sqlite3
from src.utils.db_helpers import get_user_id, get_user_reviews

# Kullanıcı bilgilerini getir
def get_user_profile(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT email, phone, address FROM users WHERE username = ?", (username,))
    profile = cursor.fetchone()
    conn.close()
    return profile

# Kullanıcı bilgilerini güncelle
def update_user_profile(username, email, phone, address):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET email = ?, phone = ?, address = ?
        WHERE username = ?
    """, (email, phone, address, username))
    conn.commit()
    conn.close()

# Profil sayfası
def profile_page():
    st.title("Profilim")
    
    username = st.session_state["username"]
    profile = get_user_profile(username)
    
    if profile:
        email, phone, address = profile
    else:
        email, phone, address = "", "", ""
    
    with st.form("profile_form"):
        st.text_input("E-posta", value=email, key="email_input")
        st.text_input("Telefon", value=phone, key="phone_input")
        st.text_area("Adres", value=address, key="address_input")
        submitted = st.form_submit_button("Bilgileri Güncelle")
    
    if submitted:
        updated_email = st.session_state["email_input"]
        updated_phone = st.session_state["phone_input"]
        updated_address = st.session_state["address_input"]
        
        update_user_profile(username, updated_email, updated_phone, updated_address)
        st.success("Bilgiler başarıyla güncellendi!")
        
    # Kullanıcının yaptığı yorumların listesi
    user_id = get_user_id(username)
    reviews = get_user_reviews(user_id)
    # Display user reviews
    st.subheader(f"Yorumlarınız ({len(reviews)})")

    if not reviews:
        st.info("Hiçbir yorumda bulunmamışsınız.")
    else:
        num_columns = 2  # Number of reviews per row
        cols = st.columns(num_columns)
        
        for index, review in enumerate(reviews):
            cafe_name = review[0]
            review_text = review[1]
            rating = review[2]
            
            col = cols[index % num_columns]
            with col:
                st.markdown(f"**{cafe_name}**")
                st.write(f"Puan: {rating} ⭐")
                st.write(f"Yorum: {review_text}")
                st.write("---")
    
