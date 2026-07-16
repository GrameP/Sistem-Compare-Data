import streamlit as st
import pandas as pd

# Tetapan muka surat web
st.set_page_config(page_title="Sistem Banding Data", layout="wide")

# Tajuk utama
st.title("Sistem Perbandingan Dokumen 📄🔍")
st.write("Muat naik dua fail (Excel, Word, atau PDF) di bawah untuk membandingkan isinya.")

# Buat dua ruangan (kiri dan kanan) untuk nampak kemas
col1, col2 = st.columns(2)

# Ruangan Kiri: Fail Pertama
with col1:
    st.subheader("Fail Pertama")
    file_1 = st.file_uploader("Muat naik Fail A", type=["pdf", "docx", "xlsx", "csv"], key="file1")

# Ruangan Kanan: Fail Kedua
with col2:
    st.subheader("Fail Kedua")
    file_2 = st.file_uploader("Muat naik Fail B", type=["pdf", "docx", "xlsx", "csv"], key="file2")

# Butang untuk mula membandingkan
if st.button("Bandingkan Dokumen", type="primary"):
    if file_1 and file_2:
        st.success("Kedua-dua fail berjaya dimuat naik! (Sistem baca teks akan ditambah di sini nanti)")
    else:
        st.warning("Sila muat naik kedua-dua fail terlebih dahulu.")
