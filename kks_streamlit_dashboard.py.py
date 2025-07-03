
import streamlit as st
import pandas as pd

# Sayfa başlığı
st.title("Kategori Kalite Skoru (KKS) Dashboard")

# Örnek veri
data = {
    "Ürün Adı": ["Siyah Deri Bot", "Kadın Çanta", "Bluetooth Kulaklık", "Erkek Spor Ayakkabı", "Laptop Çantası"],
    "Kategori": ["Kadın Bot", "Kadın Çanta", "Elektronik", "Erkek Ayakkabı", "Aksesuar"],
    "Açıklama Uzunluğu (karakter)": [120, 50, 200, 30, 90],
    "Görsel Sayısı": [3, 1, 4, 0, 2],
    "Teknik Özellik Sayısı": [4, 2, 5, 1, 3],
    "Doğru Kategori Uygunluğu (%)": [95, 80, 90, 60, 75],
    "Ekleyen": ["Satıcı", "İç Çalışan", "Satıcı", "İç Çalışan", "Satıcı"]
}

df = pd.DataFrame(data)

# KKS hesaplama fonksiyonu
def calculate_kks(row):
    desc_score = min(row["Açıklama Uzunluğu (karakter)"] / 200, 1) * 25
    image_score = min(row["Görsel Sayısı"] / 3, 1) * 20
    tech_score = min(row["Teknik Özellik Sayısı"] / 5, 1) * 25
    category_score = (row["Doğru Kategori Uygunluğu (%)"] / 100) * 30
    total_score = desc_score + image_score + tech_score + category_score
    return round(total_score, 1)

df["Kategori Kalite Skoru (KKS)"] = df.apply(calculate_kks, axis=1)

# Filtre
filter_option = st.selectbox("Ekleyen filtresi:", ["Tümü", "Satıcı", "İç Çalışan"])
if filter_option != "Tümü":
    df = df[df["Ekleyen"] == filter_option]

# Tablo gösterimi
st.dataframe(df)

# Ortalama skorları göster
avg_scores = df.groupby("Ekleyen")["Kategori Kalite Skoru (KKS)"].mean().reset_index()
st.subheader("Ortalama KKS Skoru (Ekleyen Bazlı)")
st.dataframe(avg_scores)
