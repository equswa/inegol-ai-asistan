import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Ayarları
api_anahtarim = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_anahtarim)
model = genai.GenerativeModel('gemini-2.5-flash')

# 2. Sayfa Ayarları (Sayfayı biraz daha genişlettik)
st.set_page_config(page_title="AI Marketing Pro", page_icon="⬛", layout="centered")

# 3. Arayüz Dili Sözlüğü
arayuz_dilleri = {
    "Türkçe": {
        "ayar_baslik": "⚙️ SİSTEM AYARLARI",
        "arayuz_dili": "Arayüz Dili / App Language",
        "tema_baslik": "⬛ KURUMSAL KİMLİK",
        "logo": "Logo URL",
        "arka_plan": "Arka Plan Görseli (URL)",
        "renk_yazi": "Vurgu Rengi",
        "baslik": "AI PAZARLAMA ASİSTANI",
        "alt_baslik": "Kurumsal Yapay Zeka İçerik Motoru",
        "foto_yukle": "📸 Ürün Görselini Yükleyin",
        "hedef_pazar": "HEDEF PAZAR VE STRATEJİ",
        "platform": "Yayın Platformu",
        "ton": "Marka Ses Tonu",
        "cikti_dili": "Çıktı Dili",
        "urun_detay": "ÜRÜN BİLGİLERİ",
        "urun_adi": "Ürün Adı",
        "fiyat": "Etiket Fiyatı",
        "ozellikler": "Teknik ve Estetik Özellikler",
        "buton_uret": "METNİ OLUŞTUR",
        "buton_indir": "DOSYAYI İNDİR",
        "bekle": "Sistem analiz ediyor, lütfen bekleyin...",
        "hata": "Lütfen ürün adı ve fiyat alanlarını doldurun.",
        "basari": "İşlem Başarılı. Metin Hazır."
    },
    "English": {
        "ayar_baslik": "⚙️ SYSTEM SETTINGS",
        "arayuz_dili": "App Language / Arayüz Dili",
        "tema_baslik": "⬛ BRAND IDENTITY",
        "logo": "Logo URL",
        "arka_plan": "Background Image URL",
        "renk_yazi": "Accent Color",
        "baslik": "AI MARKETING ASSISTANT",
        "alt_baslik": "Enterprise AI Content Engine",
        "foto_yukle": "📸 Upload Product Image",
        "hedef_pazar": "TARGET MARKET & STRATEGY",
        "platform": "Publishing Platform",
        "ton": "Brand Voice",
        "cikti_dili": "Output Language",
        "urun_detay": "PRODUCT DETAILS",
        "urun_adi": "Product Name",
        "fiyat": "Listed Price",
        "ozellikler": "Technical & Aesthetic Specs",
        "buton_uret": "GENERATE CONTENT",
        "buton_indir": "DOWNLOAD FILE",
        "bekle": "System is analyzing, please wait...",
        "hata": "Please fill in the product name and price fields.",
        "basari": "Operation Successful. Content Ready."
    }
}

# Sol Menü
st.sidebar.markdown("### 🌐 GLOBAL")
secilen_arayuz = st.sidebar.selectbox("Arayüz Dili / App Language", ["Türkçe", "English"])
dil = arayuz_dilleri[secilen_arayuz]

st.sidebar.markdown(f"### {dil['tema_baslik']}")
logo_linki = st.sidebar.text_input(dil['logo'], "https://cdn-icons-png.flaticon.com/512/3303/3303100.png")
arkaplan_resmi = st.sidebar.text_input(dil['arka_plan'], placeholder="https://...")
vurgu_rengi = st.sidebar.color_picker(dil['renk_yazi'], "#1a252f")

# 4. DÜZELTİLMİŞ CSS: İkonları bozmayan ve nefes alan tasarım
bg_css = f"background-image: url('{arkaplan_resmi}'); background-size: cover; background-attachment: fixed; background-position: center;" if arkaplan_resmi else f"background-color: #eaeced;"

st.markdown(f"""
<style>
    /* Arka Plan */
    .stApp {{
        {bg_css}
    }}
    
    /* FONT DÜZELTMESİ: Sol üstteki ikonları bozmamak için sadece yazıları hedefliyoruz */
    p, h1, h2, h3, h4, label, input, textarea, .stMarkdown {{
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}
    
    /* İÇ İÇE GİRME DÜZELTMESİ: Kutuya üstten boşluk (margin/padding) vererek butonlardan uzaklaştırdık */
    .block-container {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 3rem;
        padding-top: 4.5rem !important; /* Sol üstteki menü butonuna yer açar */
        margin-top: 2rem; /* Sayfayı üstten biraz aşağı iter */
        max-width: 850px; /* Kutunun genişliğini derli toplu yapar */
        border-radius: 4px; /* Hafif yumuşatılmış keskinlik */
        box-shadow: 0px 15px 40px rgba(0,0,0,0.15); /* Derinlik veren gölge */
        border-top: 6px solid {vurgu_rengi}; 
    }}

    /* Başlıklar */
    h1 {{
        color: {vurgu_rengi};
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 800;
        font-size: 26px !important;
        margin-bottom: 0px;
    }}
    h3 {{
        color: #34495e;
        font-size: 15px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 2px solid #f0f2f5; /* Çizgiyi yumuşattık */
        padding-bottom: 8px;
        margin-top: 30px; /* Bölümler arasına nefes alma payı */
    }}

    /* Aksiyon Butonu */
    div.stButton > button:first-child {{
        background-color: {vurgu_rengi};
        color: white !important;
        border-radius: 2px;
        border: none;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: 1px;
        width: 100%;
        margin-top: 20px; /* Butonu yukarıdan ayırdık */
        transition: background-color 0.3s;
    }}
    div.stButton > button:first-child:hover {{
        background-color: #2c3e50;
    }}
    
    /* Sol Menü Başlık Çizgisini Kaldırma (Daha temiz görünüm için) */
    section[data-testid="stSidebar"] h3 {{
        border-bottom: none;
        margin-top: 15px;
    }}
</style>
""", unsafe_allow_html=True)

# 5. Başlık ve İçerik Düzeni
col_logo, col_baslik = st.columns([1, 6])
with col_logo:
    if logo_linki:
        st.image(logo_linki, width=75)
with col_baslik:
    st.markdown(f"<h1>{dil['baslik']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #7f8c8d; font-size: 14px; margin-top: -10px;'>{dil['alt_baslik']}</p>", unsafe_allow_html=True)

# 6. Uygulama Ana Gövdesi
yuklenen_fotograf = st.file_uploader(dil['foto_yukle'], type=["jpg", "jpeg", "png"])
resim = None
if yuklenen_fotograf is not None:
    resim = Image.open(yuklenen_fotograf)
    st.image(resim, use_container_width=True)

st.markdown(f"### {dil['hedef_pazar']}")
col1, col2, col3 = st.columns(3)
with col1:
    platform = st.selectbox(dil['platform'], ["Instagram", "WhatsApp", "E-Commerce / Web"])
with col2:
    ses_tonu = st.selectbox(dil['ton'], ["Energetic & Emoji", "Luxury & Corporate", "Short & Direct"])
with col3:
    hedef_dil = st.selectbox(dil['cikti_dili'], ["Türkçe", "English", "Arabic", "Russian", "German", "Spanish", "French"])

st.markdown(f"### {dil['urun_detay']}")
urun_adi = st.text_input(dil['urun_adi'])
fiyat = st.text_input(dil['fiyat'])
ozellikler = st.text_area(dil['ozellikler'])

# 7. İşlem Motoru
if st.button(dil['buton_uret']):
    if urun_adi and fiyat:
        with st.spinner(dil['bekle']):
            emir = f"You are a visionary marketing expert making global sales. Product: {urun_adi}. Price: {fiyat}. Specs: {ozellikler}. Write this content strictly in {hedef_dil} language, suitable for '{platform}' format, and with a '{ses_tonu}' tone."
            if platform == "Instagram":
                emir += " Include popular relevant hashtags at the end."
            elif platform == "WhatsApp":
                emir += " Make it a direct, polite message to a customer without hashtags."

            if resim is not None:
                emir += " Also analyze the provided image; perfectly blend the color, style, and texture details into the marketing copy."
                cevap = model.generate_content([emir, resim])
            else:
                cevap = model.generate_content(emir)
            
            st.success(dil['basari'])
            st.write(cevap.text)
            
            st.download_button(
                label=dil['buton_indir'],
                data=cevap.text,
                file_name=f"content_{hedef_dil.lower()}.txt",
                mime="text/plain"
            )
    else:
        st.warning(dil['hata'])
