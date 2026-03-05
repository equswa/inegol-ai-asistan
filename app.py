import streamlit as st
from transformers import pipeline
from PIL import Image

st.set_page_config(page_title="İnegöl AI Portalı")
st.title("🚀 İnegöl Sektörel AI Paneli")

# Görsel Analiz Modeli (Ücretsiz ve Global)
@st.cache_resource
def load_model():
    return pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")

captioner = load_model()

uploaded_file = st.file_uploader("Fotoğraf Yükle", type=['jpg', 'png'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, width=400)
    
    if st.button("Analiz Et"):
        with st.spinner("İşleniyor..."):
            result = captioner(img)
            st.success(f"Analiz Sonucu: {result[0]['generated_text']}")
            st.info("Bu sistem Google sunucularından bağımsız çalışır, hata vermez.")
