import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Ayarları (Şifremiz yine güvenli kasadan çekiliyor)
api_anahtarim = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_anahtarim)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Sayfa Tasarımı
st.set_page_config(page_title="İnegöl AI Asistan Pro", page_icon="🛋️")
st.title("🛋️ İnegöl AI Asistan PRO")
st.write("Ürün bilgilerinizi girin, fotoğraf yükleyin ve platformu seçin. Yapay zeka sizin için en uygun metni yazsın!")
st.markdown("---")

# 3. Fotoğraf Yükleme Alanı
yuklenen_fotograf = st.file_uploader("📸 Mobilyanın Fotoğrafını Yükleyin (İsteğe Bağlı)", type=["jpg", "jpeg", "png"])

resim = None
if yuklenen_fotograf is not None:
    resim = Image.open(yuklenen_fotograf)
    st.image(resim, caption="Yüklenen Fotoğraf", use_container_width=True)

# 4. YENİ BÖLÜM: Açılır Menüler (Platform ve Ses Tonu)
st.markdown("### 🎯 Hedef Kitle ve Platform")
col1, col2 = st.columns(2) # Ekranı yan yana iki sütuna bölüyoruz ki şık dursun

with col1:
    platform = st.selectbox("Nerede Paylaşacaksınız?", 
                            ["Instagram Gönderisi", "WhatsApp Müşteri Yanıtı", "Sahibinden.com / E-Ticaret"])

with col2:
    ses_tonu = st.selectbox("Nasıl Bir Dil Kullanılsın?", 
                            ["Samimi ve Enerjik (Emojili)", "Lüks, Ağırbaşlı ve Kurumsal", "Kısa, Öz ve İkna Edici"])

st.markdown("### 📝 Ürün Detayları")
# 5. Kullanıcıdan Bilgi Alma
urun_adi = st.text_input("Ürün Adı", placeholder="Örn: Lüks Chester Takım")
fiyat = st.text_input("Fiyat", placeholder="Örn: 45.000 TL")
ozellikler = st.text_area("Ek Özellikler (Varsa)", placeholder="Örn: Leke tutmaz kumaş, gürgen iskelet")

# 6. İşlem Butonu
if st.button("🚀 Akıllı Reklam Metni Oluştur"):
    if urun_adi and fiyat:
        with st.spinner("Yapay zeka analiz ediyor ve metni yazıyor, lütfen bekleyin..."):
            
            # Güncellenmiş Dinamik Emrimiz (Prompt)
            emir = f"Sen İnegöl'de çok başarılı bir mobilya mağazası sahibisin. "
            emir += f"Müşteriye sunulacak ürün: {urun_adi}. Fiyat: {fiyat}. Özellikler: {ozellikler}. "
            
            # Seçilen platform ve tona göre emri arka planda şekillendiriyoruz
            emir += f"\n\nÖNEMLİ GÖREV: Bu metni kesinlikle bir '{platform}' formatına uygun olarak yaz. "
            emir += f"Kullanacağın dil, üslup ve ses tonu tam olarak '{ses_tonu}' olmalı. "
            
            if platform == "Instagram Gönderisi":
                emir += "Metnin sonuna #inegölmobilya #mobilyadekorasyon gibi popüler hashtagler ekle."
            elif platform == "WhatsApp Müşteri Yanıtı":
                emir += "Metin doğrudan müşteriye hitap eden, 'Merhaba' ile başlayan ve soruları varsa sormasını rica eden kısa bir mesaj formatında olsun. Hashtag kullanma."
            elif platform == "Sahibinden.com / E-Ticaret":
                emir += "Metin çok daha resmi, madde madde özellikleri sayan ve güven veren bir ürün açıklaması formatında olsun."

            # Eğer fotoğraf yüklendiyse
            if resim is not None:
                emir += " Ayrıca sana gönderdiğim bu mobilya fotoğrafını detaylıca incele. Rengini, tarzını, kumaş dokusunu ve malzeme yapısını analiz et. Bu görsel detayları da seçtiğim ses tonuna uygun bir şekilde metne yedir."
                cevap = model.generate_content([emir, resim])
            else:
                cevap = model.generate_content(emir)
            
            # Sonucu Göster
            st.success(f"İşte {platform} için {ses_tonu} formatındaki metniniz:")
            st.write(cevap.text)
    else:
        st.warning("Lütfen en azından Ürün Adı ve Fiyat bilgilerini doldurun!")
