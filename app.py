import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API ANAHTARIN (Kendi anahtarını tırnak içine yaz)
API_KEY = "AIzaSyCqyzabnJT31c0iNaAqb5Y5JSs0VuAXS0Y"

# Yapılandırma
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"API Bağlantı Hatası: {e}")

# Sayfa Ayarları
st.set_page_config(page_title="İnegöl Mobilya AI", layout="wide")

st.title("🪑 İnegöl Mobilya AI Reklam Asistanı")
st.write("Fotoğrafı yükleyin, istediğiniz dilde profesyonel reklam metnini alın.")

# Yan Menü - Dil ve Ayarlar
st.sidebar.header("⚙️ Ayarlar")
dil = st.sidebar.selectbox("Reklam Dili:", ["Türkçe", "English", "العربية (Arapça)", "Deutsch"])
ton = st.sidebar.selectbox("Yazım Tonu:", ["Lüks & Seçkin", "Samimi & Sıcak", "Modern & Minimalist"])

# Fotoğraf Yükleme
foto = st.file_uploader("Mobilya Fotoğrafı Seçin", type=['jpg', 'jpeg', 'png'])

if foto:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        resim = Image.open(foto)
        st.image(resim, caption="Yüklenen Ürün", use_container_width=True)
    
    with col2:
        if st.button(f"{dil} Dilinde Reklam Yaz"):
            with st.spinner("Yapay zeka analiz ediyor..."):
                try:
                    # Gelişmiş Prompt
                    komut = f"""
                    Sen bir dünya çapında mobilya pazarlama uzmanısın. 
                    Bu görseldeki mobilyayı analiz et ve şu özelliklere göre bir reklam metni yaz:
                    - Dil: {dil}
                    - Yazım Tonu: {ton}
                    - Hedef: Instagram ve Facebook reklamları için yüksek etkileşim.
                    - Detaylar: Mobilyanın kumaş dokusu, işçiliği ve tasarım kalitesine vurgu yap.
                    """
                    
                    response = model.generate_content([komut, resim])
                    
                    st.success(f"✅ {dil} Reklam Metni Hazır!")
                    st.text_area("Kopyalamak İçin Metin:", value=response.text, height=300)
                    
                except Exception as e:
                    st.error("Bir hata oluştu. Lütfen API anahtarınızı ve internetinizi kontrol edin.")
                    st.code(str(e))

# Alt Bilgi
st.markdown("---")
st.caption("İnegöl Mobilya Sektörü İçin Özel Olarak Geliştirilmiştir.")
