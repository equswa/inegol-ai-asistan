import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API ANAHTARIN
API_KEY = "AIzaSyBb4SsVo6SfaQ6nwrRyb3--QlnMvDsOCP0"

# Google Yapılandırması
try:
    genai.configure(api_key=API_KEY)
    # Görsel okuma için en garanti model
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Bağlantı Hatası: {e}")

st.set_page_config(page_title="İnegöl AI Portalı", layout="centered")
st.title("🚀 İnegöl Sektörel AI Paneli")

# Basit Arayüz
sektor = st.sidebar.selectbox("Sektör Seçin:", ["Mobilya", "Emlak", "Oto Galeri"])
uploaded_file = st.file_uploader("Fotoğrafı Buraya Yükle", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=400, caption="Analiz Edilecek Görsel")
    
    if st.button("Hadi Reklam Yaz"):
        with st.spinner("Yapay zeka analiz ediyor..."):
            try:
                # İÇERİK GÖNDERME (En Yeni Format)
                response = model.generate_content([f"{sektor} için reklam yaz", img])
                st.success("✅ İŞLEM BAŞARILI!")
                st.write(response.text)
            except Exception as e:
                st.error(f"Hata detayı: {e}")
