import streamlit as st
import pandas as pd
import language_tool_python

st.set_page_config(page_title="Akıllı Katalog Analizi", layout="wide")
st.title("📦 Akıllı Katalog Denetimi ve Kategori Öneri Sistemi")

uploaded_file = st.file_uploader("Excel dosyasını yükleyin (ürün listesi)", type=["xlsx"])

kategori_altkategori = {
    "Elektronik": ["Kulaklık", "Telefon", "Bilgisayar", "Şarj Aleti"],
    "Giyim": ["Elbise", "Mont", "Pantolon", "Gömlek"],
    "Ayakkabı": ["Spor Ayakkabı", "Bot", "Çizme"]
}

kelime_kategori_haritasi = {
    "kulaklık": "Elektronik",
    "bluetooth": "Elektronik",
    "şarj": "Elektronik",
    "pantolon": "Giyim",
    "elbise": "Giyim",
    "gömlek": "Giyim",
    "mont": "Giyim",
    "ayakkabı": "Ayakkabı",
    "bot": "Ayakkabı",
    "çizme": "Ayakkabı"
}

tool = language_tool_python.LanguageTool('tr-TR')

def kategori_tahmin_et(urun_adi):
    for kelime in urun_adi.lower().split():
        for anahtar, kategori in kelime_kategori_haritasi.items():
            if anahtar in kelime:
                return kategori
    return "Bilinmiyor"

def kalite_analiz(df):
    analiz = []
    for idx, row in df.iterrows():
        puan = 100
        uyarilar = []

        urun_adi = str(row.get("Ürün Adı", "")).strip()
        kategori = str(row.get("Kategori", "")).strip()
        alt_kategori = str(row.get("Alt Kategori", "")).strip()
        fiyat = row.get("Fiyat", 0)
        stok = row.get("Stok Adedi", 0)
        durum = str(row.get("Listeleme Durumu", "")).strip()

        # Ürün adı uzunluğu ve tekrar
        if len(urun_adi) < 5:
            puan -= 10
            uyarilar.append("Ürün adı çok kısa.")
        if any(urun_adi.lower().count(c) >= 4 for c in set(urun_adi.lower())):
            puan -= 5
            uyarilar.append("Ürün adında harf tekrarları var.")

        # Yazım hatası kontrolü
        hatalar = tool.check(urun_adi)
        if hatalar:
            puan -= 10
            uyarilar.append("Yazım hatası tespit edildi.")
            for hata in hatalar[:1]:
                uyarilar.append(f"Öneri: {hata.message}")

        # Kategori uyumu
        if kategori not in kategori_altkategori:
            puan -= 15
            uyarilar.append(f"'{kategori}' geçersiz bir kategori.")
        elif alt_kategori not in kategori_altkategori[kategori]:
            puan -= 10
            uyarilar.append(f"'{alt_kategori}' alt kategorisi '{kategori}' ile uyumsuz.")

        # Kategori tahmini
        tahmin = kategori_tahmin_et(urun_adi)
        if tahmin != "Bilinmiyor" and tahmin != kategori:
            puan -= 10
            uyarilar.append(f"Kategori hatalı olabilir. Tahmini uygun kategori: {tahmin}")

        # Fiyat kontrolü
        if pd.isna(fiyat) or fiyat <= 0:
            puan -= 20
            uyarilar.append("Fiyat geçersiz veya girilmemiş.")

        # Stok kontrolü
        if pd.isna(stok) or stok < 0:
            puan -= 10
            uyarilar.append("Stok bilgisi eksik veya geçersiz.")

        # Durum kontrolü
        if durum not in ["Aktif", "Pasif"]:
            puan -= 5
            uyarilar.append("Listeleme durumu hatalı.")

        # Genel öneri
        genel_oneri = "Ürünü güncelleyin."
        if puan >= 90:
            genel_oneri = "Harika! Ürün iyi listelenmiş."
        elif 70 <= puan < 90:
            genel_oneri = "İyi ama bazı küçük eksikler var."
        elif 50 <= puan < 70:
            genel_oneri = "Geliştirilmeye ihtiyaç var."
        else:
            genel_oneri = "Ürün kalitesi çok düşük. Gözden geçirin."

        analiz.append({
            "Satır": idx + 2,
            "Ürün Adı": urun_adi,
            "Kategori": kategori,
            "Tahmini Kategori": tahmin,
            "Alt Kategori": alt_kategori,
            "Skor": puan,
            "Uyarılar": "; ".join(uyarilar),
            "Öneri": genel_oneri
        })

    return pd.DataFrame(analiz)

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("🔍 Yüklenen Veriler")
        st.dataframe(df)

        st.subheader("📊 Kalite + Yazım + Kategori Öneri Sonuçları")
        skor_df = kalite_analiz(df)
        st.dataframe(skor_df)

        st.download_button("📥 Sonuçları CSV olarak indir",
                           data=skor_df.to_csv(index=False).encode("utf-8"),
                           file_name="akilli_katalog_analiz.csv",
                           mime="text/csv")

    except Exception as e:
        st.error(f"Hata oluştu: {e}")