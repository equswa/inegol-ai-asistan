import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API ANAHTARIN
API_KEY = "BURAYA_API_KEYINI_YAZ"

# Yapılandırma
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Bağlantı Hatası: {e}")

st.set_page_config(page_title="İnegöl AI", layout="centered")
st.title("🚀 İnegöl Sektörel AI Paneli")

# Fotoğraf Yükleme
foto = st.file_uploader("Bir fotoğraf seçin (JPG/PNG)", type=['jpg', 'jpeg', 'png'])

if foto:
    resim = Image.open(foto)
    st.image(resim, width=400, caption="Analiz Edilecek Görsel")
    
    if st.button("Reklam Metni Yaz"):
        with st.spinner("AI Analiz Ediyor..."):
            try:
                # En güvenli veri gönderme formatı
                response = model.generate_content(["Bu görseldeki ürün için etkileyici bir reklam metni yaz.", resim])
                st.success("✅ BAŞARILI!")
                st.write(response.text)
            except Exception as e:
                st.error("Bir hata oluştu. Detay:")
                st.code(str(e))