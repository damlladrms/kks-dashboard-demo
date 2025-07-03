
import streamlit as st
import pandas as pd
import re
from difflib import get_close_matches

st.set_page_config(page_title="KKS - Katalog Kontrol Sistemi", layout="wide")
st.title("📦 Katalog Kontrol ve Doğruluk Sistemi")

uploaded_file = st.file_uploader("Excel dosyasını yükleyin (.xlsx)", type=["xlsx"])

# Doğruluk kontrol referansları
dogru_kategoriler = ['Elektronik', 'Giyim', 'Ayakkabı']
dogru_alt_kategoriler = {
    'Elektronik': ['Kulaklık', 'Telefon', 'Bilgisayar'],
    'Giyim': ['Elbise', 'Mont', 'Pantolon'],
    'Ayakkabı': ['Spor Ayakkabı', 'Topuklu Ayakkabı']
}
dogru_markalar = ['Nike', 'Zara', 'JBL', 'LC Waikiki']

def check_typo(value, correct_list):
    if pd.isna(value):
        return None
    match = get_close_matches(value, correct_list, n=1, cutoff=0.8)
    return None if match else f"'{value}' yanlış yazılmış olabilir."

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df["Hatalar / Uyarılar"] = ""

    df["Hatalar / Uyarılar"] += df["Kategori"].apply(
        lambda x: "" if x in dogru_kategoriler else f"Kategori '{x}' geçersiz. "
    )

    def alt_kontrol(row):
        kategori = row["Kategori"]
        alt = row["Alt Kategori"]
        if kategori in dogru_alt_kategoriler:
            if alt not in dogru_alt_kategoriler[kategori]:
                return f"Alt Kategori '{alt}' {kategori} ile uyumsuz. "
        return ""

    df["Hatalar / Uyarılar"] += df.apply(alt_kontrol, axis=1)

    df["Hatalar / Uyarılar"] += df["Marka"].apply(lambda x: check_typo(x, dogru_markalar) or "")

    df["Hatalar / Uyarılar"] += df["Fiyat"].apply(lambda x: "" if x > 0 else "Fiyat geçersiz. ")

    df["Hatalar / Uyarılar"] += df["Stok Adedi"].apply(lambda x: "" if x >= 0 else "Stok negatif. ")

    df["Hatalar / Uyarılar"] += df["Listeleme Durumu"].apply(
        lambda x: "" if x in ['Aktif', 'Pasif'] else f"'{x}' geçersiz durum. ")

    df["Hatalar / Uyarılar"] += df["Satıcı Adı"].apply(lambda x: "" if pd.notna(x) else "Satıcı adı boş. ")

    # Otomatik düzeltme önerileri
    df["Otomatik Düzeltme Önerisi"] = df.apply(
        lambda row: "Alt Kategori: Kulaklık" if "kulaklık" in row["Ürün Adı"].lower() and row["Alt Kategori"] != "Kulaklık" else "", axis=1
    )

    st.subheader("🔍 Katalog Analiz Sonuçları")
    st.dataframe(df, use_container_width=True)

    @st.cache_data
    def convert_df(df):
        return df.to_excel(index=False, engine='openpyxl')

    excel_data = convert_df(df)
    st.download_button("📥 Excel Raporunu İndir", data=excel_data, file_name="Katalog_Kontrol_Raporu.xlsx")
else:
    st.info("Başlamak için bir katalog dosyası yükleyin.")
