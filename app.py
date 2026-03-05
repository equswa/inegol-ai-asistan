import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Ayarlar ve API Bağlantısı
st.set_page_config(page_title="AI İş Ortağım", layout="wide")

# API Anahtarını Streamlit Secrets'tan alacağız
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.warning("⚠️ API Anahtarı henüz tanımlanmadı (Secrets ayarı bekliyor).")

# 2. Yan Menü (Sektör Seçimi)
st.sidebar.title("🚀 Sektörel AI Paneli")
sektor = st.sidebar.selectbox("Lütfen Sektör Seçin:", 
                             ["Mobilya (İnegöl)", "Emlak & Dekorasyon", "Oto Galeri"])

# 3. Ana Ekran İçeriği
st.title(f"✨ {sektor} Yapay Zeka Çözümü")

uploaded_file = st.file_uploader(f"{sektor} Fotoğrafını Yükle", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    col1, col2 = st.columns(2)
    img = Image.open(uploaded_file)
    
    with col1:
        st.subheader("📸 Yüklenen Görsel")
        st.image(img, use_column_width=True)
        
    with col2:
        st.subheader("📝 Yapay Zeka Analizi")
        if st.button("Analiz Et ve Metin Yaz"):
            with st.spinner("Gemini düşünüyor..."):
                # Sektöre göre özel komut gönderiyoruz
                prompt = f"Sen profesyonel bir {sektor} pazarlama uzmanısın. Bu görseldeki ürünü analiz et ve Instagram için etkileyici bir reklam metni yaz."
                response = model.generate_content([prompt, img])

                st.write(response.text)


