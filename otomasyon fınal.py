import pandas as pd
import google.generativeai as genai
import time

# 1. AI Bağlantısı
genai.configure(api_key="API_KEY_AIzaSyCqyzabnJT31c0iNaAqb5Y5JSs0VuAXS0Y")
model = genai.GenerativeModel('gemini-pro')

# 2. EXCEL'DEN VERİ OKUMA
print("📂 'konular.xlsx' dosyası okunuyor...")
df = pd.read_excel("konular.xlsx") # Dışarıdaki dosyayı içeri aldık!

ai_cevaplari = []

print("🤖 AI içerik üretmeye başladı. Bu biraz sürebilir...")

# Excel'deki her satır için döngü başlatıyoruz
for index, satir in df.iterrows():
    p = satir["Platform"]
    k = satir["Konu"]
    t = satir["Tür"]
    
    soru = f"{p} platformu için {k} konusunda kısa bir {t} senaryosu yazar mısın?"
    
    try:
        cevap = model.generate_content(soru)
        ai_cevaplari.append(cevap.text) # Gelen cevabı listeye ekle
        print(f"✅ Satır {index+1} tamamlandı: {p}")
        
        time.sleep(1) # Hata almamak için 1 saniye mola
    except Exception as e:
       # Mevcut hata yakalama kısmını şu şekilde değiştir:
try:
    # AI içerik üretme kodun burada
    pass 
except Exception as e:
    print(f"Satır {index} başarısız! Hata: {e}")
# 3. VERİYİ KAYDETME
df["AI_Cevabı"] = ai_cevaplari # AI'dan gelenleri yeni sütun olarak tabloya ekle
df.to_excel("Final_Icerik_Raporu.xlsx", index=False)

print("\n🏆 İŞLEM TAMAM! 'Final_Icerik_Raporu.xlsx' dosyan hazır.")