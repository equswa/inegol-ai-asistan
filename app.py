import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API ANAHTARI (Buraya Kendi Anahtarını Yapıştır)
API_KEY = "AIzaSyBb4SsVo6SfaQ6nwrRyb3--QlnMvDsOCP0"


try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Bağlantı Kurulamadı: {e}")

st.title("🚀 İnegöl Sektörel AI Asistan")

# Basit Arayüz
sektor = st.sidebar.selectbox("Sektör:", ["Mobilya", "Emlak", "Galeri"])
dosya = st.file_uploader("Fotoğraf Seç", type=['jpg','png'])

if dosya:
    resim = Image.open(dosya)
    st.image(resim, width=300)
    if st.button("Reklam Yaz"):
        try:
            cevap = model.generate_content(["Bu görsel için reklam metni yaz", resim])
            st.success(cevap.text)
        except Exception as hata:
            st.error(f"Hata detayı: {hata}")
