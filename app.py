import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Kendi API Key'ini buraya yaz
API_KEY = "AIzaSyCqyzabnJT31c0iNaAqb5Y5JSs0VuAXS0Y"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🚀 İnegöl AI Asistan")

foto = st.file_uploader("Bir fotoğraf seç", type=['jpg', 'png'])

if foto:
    resim = Image.open(foto)
    st.image(resim, width=300)
    
    if st.button("Reklam Metni Yaz"):
        try:
            # En basit ve hatasız veri gönderme yöntemi
            sonuc = model.generate_content(["Bu ürün için kısa bir reklam yaz", resim])
            st.success(sonuc.text)
        except Exception as e:
            st.error(f"Sistemsel Hata: {e}")
