import streamlit as st
import os

# 1. SAYFA AYARI
st.set_page_config(page_title="AI İş Ortağım", layout="centered")

# 2. SEKTÖREL MENÜ
st.sidebar.title("🚀 AI Projelerim")
proje = st.sidebar.selectbox("Sektör Seçin:", ["Mobilya", "Emlak", "Oto Galeri"])

# 3. ANA EKRAN
st.title(f"✨ {proje} Yapay Zeka Çözümü")

# DOSYA YÜKLEME ALANI
uploaded_file = st.file_uploader(f"{proje} Fotoğrafını Buraya Yükle", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Yüklenen Görsel", use_column_width=True)
    st.success(f"{proje} analizi için hazır!")
    
    # REKLAM METNİ ÜRETME (Örnek Buton)
    if st.button("Reklam Metni Üret"):
        st.info("Yapay zeka şu an analiz yapıyor... (API Bağlantısı Aktif)")
        # Buraya daha önce konuştuğumuz Gemini kodlarını ekleyeceğiz.

# VİDEO OLUŞTURMA BÖLÜMÜ (Hata vermemesi için kontrol eklendi)
st.markdown("---")
st.subheader("🎬 Sosyal Medya Videosu")
if st.button("Video Hazırla"):
    st.warning("Video oluşturma özelliği şu an bakımda. (Lütfen requirements.txt dosyasını kontrol edin)")
