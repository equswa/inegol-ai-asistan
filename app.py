import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API ANAHTARI
API_KEY = "AIzaSyBb4SsVo6SfaQ6nwrRyb3--QlnMvDsOCP0"

st.set_page_config(page_title="İnegöl AI Portalı", layout="wide")

# API Yapılandırması
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("API Bağlantı Hatası!")

st.title("🚀 İnegöl Sektörel AI Paneli")

sektor = st.sidebar.selectbox("Sektör:", ["Mobilya", "Emlak", "Oto Galeri"])
uploaded_file = st.file_uploader("Fotoğraf Yükle", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=400)
    
    if st.button("Reklam Yaz"):
        with st.spinner("Analiz ediliyor..."):
            # ÇÖZÜM BURADA: Önce Flash modelini dene, olmazsa Pro modeline geç
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(["Bu görsel için reklam metni yaz", img])
                st.success(response.text)
            except:
                try:
                    model = genai.GenerativeModel('gemini-pro-vision')
                    response = model.generate_content(["Bu görsel için reklam metni yaz", img])
                    st.success(response.text)
                except Exception as e:
                    st.error(f"Google servislerine şu an ulaşılamıyor. Hata: {e}")
