import streamlit as st
import geocoder
from src.utils.yelp_cafes import display_cafes_on_map

def main_page():
    # Check if the tutorial has been completed
    if not st.session_state.get("tutorial_completed", True):
        show_tutorial()
    else:
        st.title("Yakındaki Kafeleri Keşfedin")

        # IP-based geolocation
        g = geocoder.ip('me')
        if g.ok and g.latlng:
            latitude, longitude = g.latlng
            display_cafes_on_map(latitude, longitude, key_prefix="nearby_")
        else:
            st.error("Konum bilgisi alınamadı.")


def show_tutorial():
    st.title("Hoş Geldiniz!")
    st.write("Bu hızlı rehber, uygulamamızda nasıl gezinip yakınınızdaki kafeleri keşfedebileceğinizi gösterir.")
    
    with st.expander("1. Sayfalar Arasında Gezinme"):
        st.write("Sol taraftaki menü aracılığıyla ana sayfa, favori kafeler, profil ve daha pek çok sayfaya geçiş yapabilirsiniz.")

    with st.expander("2. Konum Bazlı Kafe Keşfi"):
        st.write("Uygulama, bulunduğunuz konuma göre size en yakın kafeleri listeler. Harita üzerinde konumunuzu ve kafeleri görebilirsiniz.")

    with st.expander("3. Favori Kafe Ekleme"):
        st.write("İlginizi çeken kafeleri favorilerinize ekleyip daha sonra hızlıca ulaşabilirsiniz.")

    with st.expander("4. Yorum ve Puanlama"):
        st.write("Kafeler hakkında yorum yapıp puan verebilir, diğer kullanıcıların deneyimlerinden yararlanabilirsiniz.")

    with st.expander("5. Geri Bildirim"):
        st.write("Uygulama hakkında düşüncelerinizi bizimle paylaşabilir, geliştirme sürecine katkıda bulunabilirsiniz.")

    st.write("Hazırsanız başlayalım!")
    if st.button("Başla"):
        st.session_state["tutorial_completed"] = True
        st.rerun()
