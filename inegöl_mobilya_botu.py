import streamlit as st
import google.generativeai as genai
from PIL import Image # YENİ: Fotoğrafları okuyabilmek için ekledik

# 1. API Ayarları (Şifremiz artık güvenli kasadan geliyor)
api_anahtarim = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_anahtarim)
model = genai.GenerativeModel('gemini-2.5-flash') # Bu model hem metin hem fotoğraf anlayabilir!

# 2. Sayfa Tasarımı
st.set_page_config(page_title="İnegöl AI Asistan Pro", page_icon="🛋️")
st.title("🛋️ İnegöl AI Asistan PRO")
st.write("Ürün bilgilerinizi girin ve **fotoğrafını yükleyin**. Yapay zeka fotoğrafı inceleyip en iyi reklamı yazsın!")
st.markdown("---")

# 3. YENİ BÖLÜM: Fotoğraf Yükleme Alanı
yuklenen_fotograf = st.file_uploader("📸 Mobilyanın Fotoğrafını Yükleyin (İsteğe Bağlı)", type=["jpg", "jpeg", "png"])

resim = None
if yuklenen_fotograf is not None:
    resim = Image.open(yuklenen_fotograf)
    st.image(resim, caption="Yüklenen Fotoğraf", use_container_width=True) # Fotoğrafı ekranda göster

# 4. Kullanıcıdan Bilgi Alma
urun_adi = st.text_input("Ürün Adı", placeholder="Örn: Lüks Chester Takım")
fiyat = st.text_input("Fiyat", placeholder="Örn: 45.000 TL")
ozellikler = st.text_area("Ek Özellikler (Varsa)", placeholder="Örn: Leke tutmaz kumaş")

# 5. İşlem Butonu
if st.button("🚀 Akıllı Reklam Metni Oluştur"):
    if urun_adi and fiyat:
        with st.spinner("Yapay zeka fotoğrafı ve bilgileri inceliyor, lütfen bekleyin..."):
            
            # Temel Emrimiz
            emir = f"Sen İnegöl'de çok başarılı bir mobilya mağazası sahibisin. Müşterileri etkileyecek bir Instagram reklam metni yaz. Ürün: {urun_adi}, Fiyat: {fiyat}, Ek Özellikler: {ozellikler}. Metnin sonuna #inegölmobilya #mobilyadekorasyon gibi popüler hashtagler ekle."
            
            # Eğer fotoğraf yüklendiyse, emrimizi fotoğrafı da inceleyecek şekilde güncelliyoruz
            if resim is not None:
                emir += " Sana gönderdiğim bu mobilya fotoğrafını detaylıca incele. Rengini, tarzını (modern, avangart vb.), kumaş hissiyatını ve ayak yapısını analiz et. Bu görsel detayları reklam metnine coşkulu bir dille yedirerek müşterinin gözünde canlandırmasını sağla."
                # Hem emri hem resmi yapay zekaya gönderiyoruz
                cevap = model.generate_content([emir, resim])
            else:
                # Resim yoksa sadece metni gönderiyoruz
                cevap = model.generate_content(emir)
            
            # Sonucu Göster
            st.success("İşte Profesyonel Reklam Metniniz Hazır!")
            st.write(cevap.text)
    else:
        st.warning("Lütfen en azından Ürün Adı ve Fiyat bilgilerini doldurun!")