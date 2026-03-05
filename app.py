import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API ANAHTARIN (Tırnak içine yaz)
API_KEY = "BURAYA_KENDI_API_KEYINI_YAZ"

# Başlık ve Ayarlar
st.set_page_config(page_title="İnegöl AI Asistan", layout="centered")
st.title("🚀 İnegöl Sektörel AI Paneli")

# API Yapılandırması
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API Yapılandırma Hatası: {e}")

# Basit Yükleme Alanı
foto = st.file_uploader("Fotoğraf Yükle (JPG/PNG)", type=['jpg', 'jpeg', 'png'])

if foto:
    resim = Image.open(foto)
    st.image(resim, width=350, caption="Yüklenen Görsel")
    
    if st.button("Reklam Metni Oluştur"):
        with st.spinner("AI Analiz Ediyor..."):
            try:
                # Gemini'ye en güvenli veri gönderme formatı
                response = model.generate_content(["Bu görseldeki ürünü analiz et ve etkileyici bir reklam metni yaz.", resim])
                st.success("✅ İŞLEM BAŞARILI!")
                st.write(response.text)
            except Exception as e:
                # Hata neyse burada açıkça göreceğiz
                st.error("Bir sorun oluştu.")
                st.code(str(e)) # Hatayı kod kutusunda gösterir
