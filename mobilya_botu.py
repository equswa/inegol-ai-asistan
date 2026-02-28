import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Ayarları
api_anahtarim = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_anahtarim)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Sayfa Tasarımı ve YENİ: CSS ile Makyajlama
st.set_page_config(page_title="İnegöl AI Asistan Pro", page_icon="🛋️", layout="centered")

# CSS Kodlarımızı Uygulamaya Enjekte Ediyoruz
st.markdown("""
<style>
    /* Arka plan rengini hafif ve modern bir gri yapalım */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Ana Başlık Tasarımı */
    h1 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
        text-align: center;
    }
    
    /* Oluştur Butonunun Tasarımı (Bordo/Kırmızı Tonları - İnegöl Mobilyasına Uygun Lüks Hissiyat) */
    div.stButton > button:first-child {
        background-color: #8b0000;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s;
    }
    
    /* Butonun üzerine mouse ile gelindiğinde olacaklar */
    div.stButton > button:first-child:hover {
        background-color: #a52a2a;
        transform: scale(1.02);
    }
    
    /* İndirme Butonunun Tasarımı (Yeşil Tonları) */
    div.stDownloadButton > button:first-child {
        background-color: #2e8b57;
        color: white;
        border-radius: 8px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 3. YENİ BÖLÜM: Logo ve Başlık Yan Yana
col_logo, col_baslik = st.columns([1, 5]) # Ekranı 1'e 5 oranında ikiye böldük

with col_logo:
    # İnternetten şık bir mobilya ikonu çekiyoruz (Bunu sonra kendi logonla değiştirebilirsin)
    st.image("https://cdn-icons-png.flaticon.com/512/3303/3303100.png", width=80)

with col_baslik:
    st.title("İnegöl AI Asistan PRO")
    
st.markdown("<p style='text-align: left; color: #7f8c8d; font-size: 16px; margin-top: -15px;'>Yapay zeka destekli profesyonel pazarlama metinleri saniyeler içinde hazır.</p>", unsafe_allow_html=True)
st.markdown("---"))

# 4. Fotoğraf Yükleme Alanı
yuklenen_fotograf = st.file_uploader("📸 Mobilyanın Fotoğrafını Yükleyin (İsteğe Bağlı)", type=["jpg", "jpeg", "png"])

resim = None
if yuklenen_fotograf is not None:
    resim = Image.open(yuklenen_fotograf)
    # Fotoğrafın köşelerini yumuşatarak şık göstermek için CSS ayarı
    st.image(resim, caption="Analiz Edilecek Görsel", use_container_width=True)

# 5. Açılır Menüler
st.markdown("### 🎯 Strateji Belirleme")
col1, col2, col3 = st.columns(3)

with col1:
    platform = st.selectbox("Platform", ["Instagram Gönderisi", "WhatsApp", "Sahibinden/Web"])
with col2:
    ses_tonu = st.selectbox("Ses Tonu", ["Samimi (Emojili)", "Lüks ve Kurumsal", "Kısa ve Öz"])
with col3:
    hedef_dil = st.selectbox("Dil", ["Türkçe", "İngilizce", "Arapça", "Rusça"])

st.markdown("### 📝 Ürün Detayları")
urun_adi = st.text_input("Ürün Adı", placeholder="Örn: Modern Venedik Koltuk Takımı")
fiyat = st.text_input("Fiyat", placeholder="Örn: 45.000 TL")
ozellikler = st.text_area("Özellikler", placeholder="Örn: Silinebilir kadife kumaş, ceviz ayak...")

# 6. İşlem Butonu ve Çıktı
if st.button("🚀 Akıllı Reklam Metni Oluştur"):
    if urun_adi and fiyat:
        with st.spinner("Yapay zeka sihrini konuşturuyor..."):
            
            emir = f"Sen Türkiye'den dünyaya ihracat yapan vizyoner bir mobilya pazarlama uzmanısın. Ürün: {urun_adi}. Fiyat: {fiyat}. Özellikler: {ozellikler}. Bu metni kesinlikle {hedef_dil} dilinde, '{platform}' formatında ve '{ses_tonu}' üslubunda yaz."
            
            if platform == "Instagram Gönderisi":
                emir += " Metnin sonuna popüler mobilya hashtagleri ekle."
            elif platform == "WhatsApp":
                emir += " Doğrudan müşteriye hitap eden, samimi bir sohbet formatında olsun."

            if resim is not None:
                emir += " Ayrıca sana gönderdiğim fotoğrafı incele; renk, tarz ve doku analizini metne profesyonelce yedir."
                cevap = model.generate_content([emir, resim])
            else:
                cevap = model.generate_content(emir)
            
            st.success("✨ İşlem Tamamlandı!")
            st.write(cevap.text)
            
            st.download_button(
                label="📥 Metni Dosya Olarak İndir",
                data=cevap.text,
                file_name="reklam_metni.txt",
                mime="text/plain"
            )
    else:
        st.warning("Lütfen Ürün Adı ve Fiyat bilgilerini doldurun!")

