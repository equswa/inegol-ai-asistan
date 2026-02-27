import streamlit as st
import google.generativeai as genai

# 1. API Ayarları (BURAYA KENDİ ANAHTARINI YAPŞTIR)
api_anahtarim = st.secrets["GOOGLE_API_KEY"] 
genai.configure(api_key=api_anahtarim)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Sayfanın Başlığı ve Tasarımı
st.set_page_config(page_title="İnegöl AI Asistan", page_icon="🛋️")
st.title("🛋️ İnegöl Mobilya Reklam Asistanı")
st.write("Ürün bilgilerinizi girin, yapay zeka saniyeler içinde Instagram reklamınızı yazsın!")
st.markdown("---") # Ekrana çizgi çeker

# 3. Kullanıcıdan Bilgi Alma Kutucukları (Siyah ekran yerine modern kutular)
urun_adi = st.text_input("Ürün Adı", placeholder="Örn: Lüks Chester Takım")
fiyat = st.text_input("Fiyat", placeholder="Örn: 45.000 TL")
ozellikler = st.text_area("Özellikler", placeholder="Örn: Leke tutmaz kumaş, gürgen iskelet")

# 4. İşlem Butonu
if st.button("🚀 Reklam Metni Oluştur"):
    # Eğer kutular boş değilse çalışsın
    if urun_adi and fiyat and ozellikler:
        with st.spinner("Yapay zeka metni hazırlıyor, lütfen bekleyin..."):
            
            # Yapay Zekaya Emri Veriyoruz
            emir = f"Sen İnegöl'de çok başarılı bir mobilya mağazası sahibisin. Müşterileri etkileyecek, samimi ve ikna edici bir Instagram reklam metni yaz. Ürün: {urun_adi}, Özellikleri: {ozellikler}, Fiyatı: {fiyat}. Metin kısa, bol emojili ve hemen satın alma isteği uyandıran bir dilde olsun."
            
            cevap = model.generate_content(emir)
            
            # Sonucu Ekranda Şık Bir Şekilde Göster
            st.success("İşte Reklam Metniniz Hazır!")
            st.write(cevap.text)
    else:
        # Eğer kullanıcı kutuları boş bırakıp butona basarsa uyarı ver
        st.warning("Lütfen tüm alanları doldurun!")