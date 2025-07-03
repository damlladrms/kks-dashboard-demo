import streamlit as st
import pandas as pd

st.set_page_config(page_title="KKS Dashboard", layout="wide")

st.title("Yüklenen Veri")

uploaded_file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"])

def analiz_et(df):
    sorunlar = []

    # Kategori-Alt Kategori ilişkisi
    kategori_altkategori = {
        "Elektronik": ["Kulaklık", "Telefon", "Bilgisayar"],
        "Giyim": ["Elbise", "Mont", "Pantolon"],
        "Ayakkabı": ["Spor Ayakkabı", "Bot"]
    }

    for idx, row in df.iterrows():
        urun_adi = row["Ürün Adı"]
        kategori = row["Kategori"]
        alt_kategori = row["Alt Kategori"]
        fiyat = row["Fiyat"]
        stok = row["Stok Adedi"]
        durum = row["Listeleme Durumu"]

        # 1. Kategori - Alt kategori uyumu
        if kategori in kategori_altkategori:
            if alt_kategori not in kategori_altkategori[kategori]:
                sorunlar.append((idx, "Alt kategori '{}' kategorisine uymuyor".format(alt_kategori)))
        else:
            sorunlar.append((idx, "Kategori '{}' tanımsız".format(kategori)))

        # 2. Fiyat kontrolü
        if pd.isna(fiyat) or fiyat <= 0:
            sorunlar.append((idx, "Fiyat geçersiz"))

        # 3. Stok kontrolü
        if pd.isna(stok) or stok < 0:
            sorunlar.append((idx, "Stok geçersiz"))

        # 4. Listeleme durumu kontrolü
        if durum not in ["Aktif", "Pasif"]:
            sorunlar.append((idx, "Listeleme durumu geçersiz"))

        # 5. Yazım kontrolü (örnek: Ürün Adı'nda 3'ten fazla aynı harf)
        for kelime in urun_adi.split():
            for harf in set(kelime.lower()):
                if kelime.lower().count(harf) >= 3:
                    sorunlar.append((idx, f"'{urun_adi}' ifadesinde '{harf}' harfi çok tekrar ediyor"))
                    break

    return sorunlar

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.dataframe(df)

        sorunlar = analiz_et(df)

        if sorunlar:
            st.subheader("Tespit Edilen Sorunlar")
            for idx, sorun in sorunlar:
                st.markdown(f"**Satır {idx + 2}**: {sorun}")
        else:
            st.success("Herhangi bir sorun tespit edilmedi. Veriler doğru görünüyor.")

    except Exception as e:
        st.error(f"Dosya okunamadı: {e}")