import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="AI İş Çözümleri Merkezi", layout="wide")

# SOL MENÜ - Proje Seçimi
st.sidebar.title("🚀 AI Projelerim")
proje = st.sidebar.selectbox("Hangi Sektör İçin Çalışalım?", 
                             ["Mobilya Studio", "Emlak Görselleştirme", "Oto Galeri AI"])

if proje == "Mobilya Studio":
    st.header("🪑 Mobilya İçerik Fabrikası")
    # Buraya daha önce yazdığımız mobilya kodlarını yapıştır...
    
elif proje == "Emlak Görselleştirme":
    st.header("🏠 Emlak & Dekorasyon AI")
    st.write("Boş ev fotoğraflarını eşyalı hale getirin (Yakında!)")
    # Buraya emlak projenin kodlarını ekleyeceksin...

elif proje == "Oto Galeri AI":
    st.header("🚗 Profesyonel Araç İlanı")
    st.write("Araç fotoğraflarının arka planını stüdyoya çevirin.")
import streamlit as st
import google.generativeai as genai
from PIL import Image
from moviepy.editor import ImageClip

# API Yapılandırması
API_KEY = "SENIN_API_KEY_BURAYA" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("🪑 AI Mobilya İçerik Fabrikası v1.0")

# Görsel Yükleme ve Analiz
orig_img = st.file_uploader("Mobilya Fotoğrafı Yükle", type=['jpg','png'])
if orig_img:
    img = Image.open(orig_img)
    if st.button("Analiz Et ve Reklam Yaz"):
        response = model.generate_content(["Bu mobilyayı analiz et ve lüks bir villa için İngilizce görsel üretim promptu yaz.", img])
        st.write(response.text)

st.markdown("---")

# Video Oluşturma
lux_img = st.file_uploader("Leonardo'dan Aldığın Lüks Görseli Yükle", type=['jpg','png'], key="lux")
if lux_img:
    if st.button("🎬 Videoyu Bulutta Render Et"):
        with open("temp.png", "wb") as f:
            f.write(lux_img.getbuffer())
        
        # Basit ve hızlı video oluşturma
        clip = ImageClip("temp.png").set_duration(5)
        clip.write_videofile("cikti.mp4", fps=24, codec="libx264")
        
        st.video("cikti.mp4")
        st.success("Video başarıyla oluşturuldu!")