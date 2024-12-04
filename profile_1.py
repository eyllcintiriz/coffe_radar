import streamlit as st
import sqlite3

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
