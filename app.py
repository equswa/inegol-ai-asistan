import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- API ANAHTARINI BURAYA YAZ (EN GARANTİ YOL) ---
API_KEY_DOKUNMA = "AIzaSyBb4SsVo6SfaQ6nwrRyb3--QlnMvDsOCP0"
 
genai.configure(api_key=API_KEY_DOKUNMA)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
# --------------------------------------------------

st.set_page_config(page_title="İnegöl AI Asistan", layout="wide")
st.title("🚀 İnegöl Sektörel AI Paneli")



# 2. Yan Menü (Sektör Seçimi)
st.sidebar.title("🚀 Sektörel AI Paneli")
sektor = st.sidebar.selectbox("Lütfen Sektör Seçin:", 
                             ["Mobilya (İnegöl)", "Emlak & Dekorasyon", "Oto Galeri"])

# 3. Ana Ekran İçeriği
st.title(f"✨ {sektor} Yapay Zeka Çözümü")

uploaded_file = st.file_uploader(f"{sektor} Fotoğrafını Yükle", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    col1, col2 = st.columns(2)
    img = Image.open(uploaded_file)
    
    with col1:
        st.subheader("📸 Yüklenen Görsel")
        st.image(img, use_column_width=True)
        
    with col2:
        st.subheader("📝 Yapay Zeka Analizi")
        if st.button("Analiz Et ve Metin Yaz"):
            with st.spinner("Gemini düşünüyor..."):
                # Sektöre göre özel komut gönderiyoruz
                prompt = f"Sen profesyonel bir {sektor} pazarlama uzmanısın. Bu görseldeki ürünü analiz et ve Instagram için etkileyici bir reklam metni yaz."
                response = model.generate_content([prompt, img])
                st.write(response.text)

if st.button("Analiz Et ve Metin Yaz"):
    with st.spinner("Gemini düşünüyor... Lütfen bekleyin."):
        try:
            prompt = f"Sen profesyonel bir {sektor} pazarlama uzmanısın. Bu görseldeki ürünü analiz et ve Instagram için etkileyici bir reklam metni yaz."
            response = model.generate_content([prompt, img])
            st.success("İşlem Başarılı!")
            st.write(response.text)
        except Exception as e:
            st.error(f"Bağlantı hatası oluştu: {e}")
            st.info("İpucu: API anahtarınızın aktif olduğundan ve internet bağlantınızın stabil olduğundan emin olun.")                


