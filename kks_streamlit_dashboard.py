
import streamlit as st
import pandas as pd

# Sayfa başlığı
st.set_page_config(page_title="KKS Katalog Kontrol Sistemi", layout="wide")

st.title("🧠 KKS - Katalog Kontrol Sistemi")
st.markdown("### Katalog doğruluğunu artırmak için geliştirilmiş demo dashboard")

uploaded_file = st.file_uploader("Excel dosyasını yükleyin (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.success("Dosya başarıyla yüklendi ve okundu.")

        st.subheader("Yüklenen Veri")
        st.dataframe(df, use_container_width=True)

        # Kategoride eksik değerleri kontrol et
        if "Kategori" in df.columns:
            missing = df["Kategori"].isna().sum()
            st.warning(f"🟡 Eksik kategori sayısı: {missing}")
        else:
            st.error("Kategori sütunu bulunamadı.")

        # Örnek basit analiz: Kategoriye göre ürün sayısı
        if "Kategori" in df.columns:
            st.subheader("Kategoriye Göre Ürün Dağılımı")
            category_counts = df["Kategori"].value_counts()
            st.bar_chart(category_counts)

        # Manuel kontrol için kullanıcıya işaretleme alanı
        st.subheader("Manuel Kontrol Paneli")
        if "Ürün Adı" in df.columns:
            selected_rows = st.multiselect("Kontrol edilecek ürünleri seçin", df["Ürün Adı"].tolist())
            st.write("Seçilen Ürünler:")
            st.write(selected_rows)

    except Exception as e:
        st.error(f"Bir hata oluştu: {e}")
else:
    st.info("Başlamak için bir Excel dosyası yükleyin.")
