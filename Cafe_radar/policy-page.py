import streamlit as st

def privacy_policy_page():
    st.title("Gizlilik Politikası")
    
    st.markdown("""
    ## Gizlilik Politikamız

    ### Veri Toplama
    - Uygulamamız, kullanıcı hesabı oluşturma ve yönetme amacıyla minimum düzeyde kişisel veri toplar.
    - Toplanan veriler: kullanıcı adı ve şifre
    - Hiçbir kredi kartı veya ödeme bilgisi toplanmaz

    ### Veri Kullanımı
    - Toplanan veriler yalnızca uygulama içi kullanım için kullanılır
    - Kullanıcı bilgileri üçüncü taraflarla paylaşılmaz

    ### Veri Güvenliği
    - Şifreler veritabanında güvenli bir şekilde saklanır
    - Kişisel bilgilerinizin güvenliği için gerekli önlemler alınmıştır

    ### Kullanıcı Hakları
    - Hesabınızı istediğiniz zaman silebilirsiniz
    - Kişisel verilerinizle ilgili bilgi talep edebilirsiniz

    ### İletişim
    Gizlilik politikamızla ilgili sorularınız için bize ulaşabilirsiniz.
    """)

def terms_of_service_page():
    st.title("Kullanım Şartları")
    
    st.markdown("""
    ## Kullanım Şartları

    ### Kabul Şartları
    - Uygulamayı kullanarak bu şartları kabul etmiş sayılırsınız
    - 18 yaş ve üzeri kullanıcılar için tasarlanmıştır

    ### Kullanıcı Yükümlülükleri
    - Doğru ve güncel bilgi sağlamakla yükümlüsünüz
    - Başkalarının haklarını ihlal eden içerik paylaşamazsınız
    - Uygulamanın düzgün kullanımından sorumlusunuz

    ### İçerik Politikası
    - Cafe incelemeleri ve yorumlar hakaret, tehdit veya uygunsuz içerik içeremez
    - İçerik moderasyonu yapılacaktır

    ### Hesap Güvenliği
    - Hesap bilgilerinizin gizliliğinden siz sorumlusunuz
    - Şifrenizi kimseyle paylaşmayın

    ### Sorumluluk Reddi
    - Uygulama "olduğu gibi" sunulmaktadır
    - Herhangi bir garanti verilmez

    ### Değişiklik Hakkı
    - Kullanım şartları önceden bildirimde bulunmaksızın değiştirilebilir
    """)
