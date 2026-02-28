import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Ayarları
api_anahtarim = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_anahtarim)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Sayfa Tasarımı
st.set_page_config(page_title="İnegöl AI Asistan Pro", page_icon="🛋️")
st.title("🛋️ İnegöl AI Asistan PRO")
st.write("Ürün bilgilerinizi girin, fotoğraf yükleyin ve hedef pazarınızı seçin. Yapay zeka gerisini halletsin!")
st.markdown("---")

# 3. Fotoğraf Yükleme Alanı
yuklenen_fotograf = st.file_uploader("📸 Mobilyanın Fotoğrafını Yükleyin (İsteğe Bağlı)", type=["jpg", "jpeg", "png"])

resim = None
if yuklenen_fotograf is not None:
    resim = Image.open(yuklenen_fotograf)
    st.image(resim, caption="Yüklenen Fotoğraf", use_container_width=True)

# 4. Açılır Menüler (Platform, Ses Tonu ve YENİ: Dil)
st.markdown("### 🎯 Hedef Kitle, Platform ve Dil")
col1, col2, col3 = st.columns(3) # Ekranı bu sefer 3 eşit parçaya böldük

with col1:
    platform = st.selectbox("Nerede Paylaşacaksınız?", 
                            ["Instagram Gönderisi", "WhatsApp Müşteri Yanıtı", "Sahibinden / E-Ticaret"])
with col2:
    ses_tonu = st.selectbox("Nasıl Bir Dil Kullanılsın?", 
                            ["Samimi ve Enerjik (Emojili)", "Lüks ve Kurumsal", "Kısa ve Öz"])
with col3:
    hedef_dil = st.selectbox("Hangi Dilde Yazılsın?", 
                             ["Türkçe", "İngilizce (Avrupa/ABD)", "Arapça (Orta Doğu)", "Rusça (Rusya/Türki Cumhuriyetler)"])

st.markdown("### 📝 Ürün Detayları (Türkçe Girebilirsiniz)")
# 5. Kullanıcıdan Bilgi Alma
urun_adi = st.text_input("Ürün Adı", placeholder="Örn: Lüks Chester Takım")
fiyat = st.text_input("Fiyat", placeholder="Örn: 45.000 TL / 1500 USD")
ozellikler = st.text_area("Ek Özellikler (Varsa)", placeholder="Örn: Leke tutmaz kumaş, fırınlanmış gürgen iskelet")

# 6. İşlem Butonu
if st.button("🚀 Akıllı Reklam Metni Oluştur"):
    if urun_adi and fiyat:
        with st.spinner(f"Yapay zeka analiz ediyor ve {hedef_dil} dilinde metni yazıyor, lütfen bekleyin..."):
            
            # Dinamik Emrimiz (Prompt)
            emir = f"Sen Türkiye'den tüm dünyaya ihracat yapan çok başarılı bir mobilya markası yöneticisisin. "
            emir += f"Ürün: {urun_adi}. Fiyat: {fiyat}. Özellikler: {ozellikler}. "
            
            # Seçilen platform, ton ve DİL ayarlamaları
            emir += f"\n\nÖNEMLİ GÖREV: Bu metni KESİNLİKLE {hedef_dil} dilinde yaz. "
            emir += f"Formatı bir '{platform}' formatına uygun olmalı. "
            emir += f"Üslup ve ses tonu tam olarak '{ses_tonu}' olmalı. {hedef_dil} dilinin kültürel pazarlama dinamiklerine ve doğal söyleyiş biçimlerine dikkat et. Asla makine çevirisi gibi durmasın, o dili ana dili gibi konuşan bir satış uzmanı yazmış gibi olsun."
            
            if platform == "Instagram Gönderisi":
                emir += f" Metnin sonuna o dilde popüler olan mobilya ve dekorasyon hashtagleri ekle."
            elif platform == "WhatsApp Müşteri Yanıtı":
                emir += " Metin doğrudan müşteriye hitap eden, kısa bir mesaj formatında olsun. Hashtag kullanma."

            # Eğer fotoğraf yüklendiyse
            if resim is not None:
                emir += " Ayrıca sana gönderdiğim bu mobilya fotoğrafını detaylıca incele. Rengini, tarzını, kumaş dokusunu ve malzeme yapısını analiz et. Bu görsel detayları da metne mükemmel bir şekilde yedir."
                cevap = model.generate_content([emir, resim])
            else:
                cevap = model.generate_content(emir)
            
            # Sonucu Göster
            st.success(f"İşte {hedef_dil} dilindeki profesyonel metniniz:")
            st.write(cevap.text)
            
            # YENİ BÖLÜM: Metni İndirme Butonu
            st.download_button(
                label="📥 Metni Dosya Olarak İndir",
                data=cevap.text,
                file_name="yapay_zeka_reklam_metni.txt",
                mime="text/plain"
            )
    else:
        st.warning("Lütfen en azından Ürün Adı ve Fiyat bilgilerini doldurun!")
