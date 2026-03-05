import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API ANAHTARI - BURAYI GÜNCELLE
API_KEY = "AIzaSyBb4SsVo6SfaQ6nwrRyb3--QlnMvDsOCP0"


# Gemini Ayarları
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Kurulum Hatası: {e}")

st.set_page_config(page_title="İnegöl AI Asistan", layout="wide")
st.title("🚀 İnegöl Sektörel AI Paneli")

# Yan Menü
sektor = st.sidebar.selectbox("Sektör Seçin:", ["Mobilya", "Emlak", "Oto Galeri"])

# Dosya Yükleme
uploaded_file = st.file_uploader(f"{sektor} Fotoğrafı Yükle", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Yüklenen Görsel", width=400)
    
    if st.button("Reklam Yaz"):
        with st.spinner("Yapay zeka analiz ediyor..."):
            try:
                # Prompt ve Görseli Liste Olarak Gönderiyoruz (En Garanti Yol)
                prompt = f"Sen bir {sektor} pazarlama uzmanısın. Bu görseli analiz et ve etkileyici bir reklam metni yaz."
                response = model.generate_content([prompt, img])
                
                st.success("Analiz Tamamlandı!")
                st.write(response.text)
            except Exception as e:
                st.error(f"Hata detayı: {e}")
