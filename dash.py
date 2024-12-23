import streamlit as st
import pandas as pd

# Fungsi untuk membaca file
def load_data():
    try:
        shopee = pd.read_excel("combined_with_shopee.xlsx")
        tokopedia = pd.read_excel("TOKOPEDIA_combined.xlsx")
        tiktok = pd.read_excel("toktok_combined.xlsx")
    except Exception as e:
        st.error(f"Error loading files: {e}")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong jika terjadi kesalahan

    # Rename kolom pendapatan untuk konsistensi
    shopee.rename(columns={"Harga Setelah Diskon": "Pendapatan"}, inplace=True)
    tokopedia.rename(columns={"Harga Jual (IDR)": "Pendapatan"}, inplace=True)
    tiktok.rename(columns={"SKU Subtotal After Discount": "Pendapatan"}, inplace=True)

    # Menambahkan platform ke masing-masing data
    shopee["Platform"] = "Shopee"
    tokopedia["Platform"] = "Tokopedia"
    tiktok["Platform"] = "TikTok"

    # Gabungkan semua data
    combined_data = pd.concat([shopee, tokopedia, tiktok], ignore_index=True)
    return combined_data

# Load data
data = load_data()

if not data.empty:
    # Judul Dashboard
    st.title("Dashboard Penjualan Multi-Platform")

    # Statistik Utama
    st.header("Statistik Utama")
    total_pendapatan = data["Pendapatan"].sum()
    rata_rata_pendapatan = data["Pendapatan"].mean()
    total_transaksi = data.shape[0]

    st.metric("Total Pendapatan (IDR)", f"{total_pendapatan:,.0f}")
    st.metric("Rata-rata Pendapatan per Transaksi", f"{rata_rata_pendapatan:,.0f}")
    st.metric("Total Transaksi", total_transaksi)

    # Grafik Pendapatan per Platform
    st.header("Pendapatan Berdasarkan Platform")
    pendapatan_per_platform = data.groupby("Platform")["Pendapatan"].sum().reset_index()
    st.bar_chart(pendapatan_per_platform.set_index("Platform"))

    # Tabel Data
    st.header("Detail Data Penjualan")
    st.dataframe(data)

    # Filter Data
    st.sidebar.header("Filter Data")
    platform_filter = st.sidebar.multiselect("Pilih Platform", options=data["Platform"].unique(), default=data["Platform"].unique())
    filtered_data = data[data["Platform"].isin(platform_filter)]

    st.write("Data Terfilter:")
    st.dataframe(filtered_data)
else:
    st.warning("Tidak ada data untuk ditampilkan.")
