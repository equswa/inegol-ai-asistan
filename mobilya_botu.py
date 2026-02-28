import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Ayarları
api_anahtarim = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_anahtarim)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Sayfa Ayarları
st.set_page_config(page_title="AI Pazarlama Asistanı", page_icon="✨", layout="centered")

# 3. YENİ: Gelişmiş VIP Tema ve Marka Kontrol Paneli (Sol Menü)
st.sidebar.markdown("### 🎨 VIP Marka Ayarları")
st.sidebar.write("Müşterinizin kurumsal kimliğine göre sistemi özelleştirin:")

# Logo ve Arka Plan Resmi (Link olarak)
logo_linki = st.sidebar.text_input("Logo Linki (URL)", "https://cdn-icons-png.flaticon.com/512/3303/3303100.png")
arkaplan_resmi = st.sidebar.text_input("Arka Plan Resmi Linki (URL)", placeholder="Örn: https://.../magaza.jpg")

# Renk ve Yazı Tipi Seçiciler
arkaplan_rengi = st.sidebar.color_picker("Arka Plan Rengi (Resim yoksa geçerlidir)", "#f8f9fa")
yazi_rengi = st.sidebar.color_picker("Genel Yazı ve Başlık Rengi", "#2c3e50")
yazi_tipi = st.sidebar.selectbox("Yazı Tipi (Font)", ["sans-serif", "serif", "monospace", "Arial", "Courier New"])

# 4. Dinamik CSS (Tasarım) Enjeksiyonu
# Eğer kullanıcı arka plan resmi girdiyse onu kullan, girmediyse seçilen rengi kullan
bg_css = f"background-image: url('{arkaplan_resmi}'); background-size: cover; background-attachment: fixed; background-position: center;" if arkaplan_resmi else f"background-color: {arkaplan_rengi};"

st.markdown(f"""
<style>
    /* Arka Plan Ayarı */
    .stApp {{
        {bg_css}
    }}
    
    /* Genel Yazı Rengi ve Tipi Ayarı */
    html, body, [class*="st-"], h1, h2, h3, p, label {{
        font-family: {yazi_tipi} !important;
        color: {yazi_rengi} !important;
    }}
    
    /* İçeriklerin Arka Planda Okunabilmesi İçin Hafif Şeffaf Kutu */
    .block-container {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}

    /* Buton Tasarımları */
    div.stButton > button:first-child {{
        background-color: #8b0000;
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s;
    }}
    div.stButton > button:first-child:hover {{
        background-color: #a52a2a;
        transform: scale(1.02);
    }}
</style>
""", unsafe_allow_html=True)

# 5. Logo ve Başlık
col_logo, col_baslik = st.columns([1, 4])
with col_logo:
    # Sol menüden girilen logo linkini buraya otomatik çeker
    if logo_linki:
        st.image(logo_linki, width=100)
with col_baslik:
    st.title("AI Pazarlama Asistanı")
    st.markdown(f"<p style='color: {yazi_rengi}; font-size: 16px; margin-top: -15px;'>Kurumsal yapay zeka içerik üreticiniz.</p>", unsafe_allow_html=True)

st.markdown("---")

# 6. Uygulamanın Ana Gövdesi (Resim Yükleme, Menüler vb.)
yuklenen_fotograf = st.file_uploader("📸 Mobilyanın Fotoğrafını Yükleyin", type=["jpg", "jpeg", "png"])
resim = None
if yuklenen_fotograf is not None:
    resim = Image.open(yuklenen_fotograf)
    st.image(resim, caption="Analiz Edilecek Görsel", use_container_width=True)

col1, col2, col3 = st.columns(3)
with col1:
    platform = st.selectbox("Platform", ["Instagram Gönderisi", "WhatsApp", "Sahibinden/Web"])
with col2:
    ses_tonu = st.selectbox("Ses Tonu", ["Samimi (Emojili)", "Lüks ve Kurumsal", "Kısa ve Öz"])
with col3:
    hedef_dil = st.selectbox("Dil", ["Türkçe", "İngilizce", "Arapça", "Rusça", "Almanca", "İspanyolca", "Fransızca"])

urun_adi = st.text_input("Ürün Adı", placeholder="Örn: Modern Venedik Koltuk Takımı")
fiyat = st.text_input("Fiyat", placeholder="Örn: 45.000 TL / 1200 Euro")
ozellikler = st.text_area("Özellikler", placeholder="Örn: Silinebilir kadife kumaş, ceviz ayak...")

if st.button("🚀 Akıllı Reklam Metni Oluştur"):
    if urun_adi and fiyat:
        with st.spinner("Yapay zeka sihrini konuşturuyor..."):
            emir = f"Sen Türkiye'den dünyaya ihracat yapan vizyoner bir mobilya pazarlama uzmanısın. Ürün: {urun_adi}. Fiyat: {fiyat}. Özellikler: {ozellikler}. Bu metni kesinlikle {hedef_dil} dilinde, '{platform}' formatında ve '{ses_tonu}' üslubunda yaz."
            if platform == "Instagram Gönderisi":
                emir += " Metnin sonuna popüler mobilya hashtagleri ekle."
            elif platform == "WhatsApp":
                emir += " Doğrudan müşteriye hitap eden, samimi bir sohbet formatında olsun. Hashtag kullanma."

            if resim is not None:
                emir += " Ayrıca fotoğrafı incele; renk, tarz ve doku analizini metne profesyonelce yedir."
                cevap = model.generate_content([emir, resim])
            else:
                cevap = model.generate_content(emir)
            
            st.success(f"✨ İşlem Tamamlandı!")
            st.write(cevap.text)
            
            st.download_button(
                label="📥 Metni Dosya Olarak İndir",
                data=cevap.text,
                file_name=f"reklam_{hedef_dil.lower()}.txt",
                mime="text/plain"
            )
    else:
        st.warning("Lütfen Ürün Adı ve Fiyat bilgilerini doldurun!")
