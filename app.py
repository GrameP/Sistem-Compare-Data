import streamlit as st
import pandas as pd

# Tetapan muka surat web
st.set_page_config(page_title="Sistem Banding Data", layout="wide")

st.title("Sistem Perbandingan Dokumen 📄🔍")
st.write("Muat naik dua fail di bawah untuk membandingkan isinya.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fail Pertama (A)")
    file_1 = st.file_uploader("Muat naik Fail A", type=["pdf", "docx", "xlsx", "csv"], key="file1")

with col2:
    st.subheader("Fail Kedua (B)")
    file_2 = st.file_uploader("Muat naik Fail B", type=["pdf", "docx", "xlsx", "csv"], key="file2")

# Sistem akan terus berjalan bila kedua-dua fail ada
if file_1 and file_2:
    if file_1.name.endswith(('.xlsx', '.csv')) and file_2.name.endswith(('.xlsx', '.csv')):
        try:
            # 1. Baca fail
            df1 = pd.read_csv(file_1) if file_1.name.endswith('.csv') else pd.read_excel(file_1)
            df2 = pd.read_csv(file_2) if file_2.name.endswith('.csv') else pd.read_excel(file_2)

            st.success("Kedua-dua fail berjaya dibaca!")
            st.divider()
            
            # 2. Paparan Data Asas
            st.write("### 📊 Paparan Data Asas")
            colA, colB = st.columns(2)
            with colA:
                st.dataframe(df1, height=200)
            with colB:
                st.dataframe(df2, height=200)

            st.divider()

            # 3. Tetapan Perbandingan (Pilih Lajur Secara Manual)
            st.write("### ⚙️ Tetapan Perbandingan")
            st.info("Pilih lajur dari setiap fail yang anda ingin bandingkan.")
            
            col_pilih_A, col_pilih_B = st.columns(2)
            with col_pilih_A:
                # Paparkan senarai lajur Fail A untuk dipilih
                pilihan_A = st.selectbox("Pilih lajur untuk Fail A:", df1.columns)
            with col_pilih_B:
                # Paparkan senarai lajur Fail B untuk dipilih
                pilihan_B = st.selectbox("Pilih lajur untuk Fail B:", df2.columns)

            st.divider()

            # 4. Logik Banding Data
            st.write("### 🎯 Hasil Perbandingan")
            
            # Tukar semua data dalam lajur yang dipilih kepada teks (string) supaya mudah dibanding
            # Buang data yang kosong (NaN)
            data_A = df1[pilihan_A].astype(str).dropna().tolist()
            data_B = df2[pilihan_B].astype(str).dropna().tolist()
            
            # Cari persamaan menggunakan fungsi 'set'
            persamaan = set(data_A).intersection(set(data_B))
            
            if persamaan:
                st.success(f"Terdapat {len(persamaan)} rekod yang SAMA ditemui antara kedua-dua lajur tersebut!")
                st.write("Senarai rekod yang wujud dalam kedua-dua fail:")
                
                # Tunjuk hasil dalam bentuk jadual
                df_hasil = pd.DataFrame(list(persamaan), columns=["Data Sama"])
                st.dataframe(df_hasil)
            else:
                st.warning("Tiada sebarang persamaan data ditemui antara dua lajur tersebut.")

        except Exception as e:
            st.error(f"Ralat semasa memproses fail: {e}")
            
    else:
        st.info("Sistem bacaan untuk Word dan PDF belum diaktifkan lagi.")
