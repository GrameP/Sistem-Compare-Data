import streamlit as st
import pandas as pd

# Tetapan muka surat web
st.set_page_config(page_title="Sistem Banding Data", layout="wide")

# Tajuk utama
st.title("Sistem Perbandingan Dokumen 📄🔍")
st.write("Muat naik dua fail di bawah untuk membandingkan isinya.")

# Buat dua ruangan (kiri dan kanan)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Fail Pertama (A)")
    file_1 = st.file_uploader("Muat naik Fail A", type=["pdf", "docx", "xlsx", "csv"], key="file1")

with col2:
    st.subheader("Fail Kedua (B)")
    file_2 = st.file_uploader("Muat naik Fail B", type=["pdf", "docx", "xlsx", "csv"], key="file2")

# Butang untuk mula membandingkan
if st.button("Bandingkan Dokumen", type="primary"):
    if file_1 and file_2:
        
        # --- LOGIK UNTUK FAIL EXCEL DAN CSV ---
        if file_1.name.endswith(('.xlsx', '.csv')) and file_2.name.endswith(('.xlsx', '.csv')):
            try:
                # 1. Baca fail menggunakan enjin Pandas
                if file_1.name.endswith('.csv'):
                    df1 = pd.read_csv(file_1)
                else:
                    df1 = pd.read_excel(file_1)

                if file_2.name.endswith('.csv'):
                    df2 = pd.read_csv(file_2)
                else:
                    df2 = pd.read_excel(file_2)

                st.success("Kedua-dua fail berjaya dibaca oleh sistem!")
                st.divider() # Buat garisan pemisah

                # 2. Paparkan data yang dibaca (Preview)
                st.write("### 📊 Paparan Data Asas")
                colA, colB = st.columns(2)
                with colA:
                    st.write(f"**Data Fail A** (Jumlah: {len(df1)} baris)")
                    st.dataframe(df1) # Tunjuk jadual A
                with colB:
                    st.write(f"**Data Fail B** (Jumlah: {len(df2)} baris)")
                    st.dataframe(df2) # Tunjuk jadual B

                st.divider()

                # 3. Mula Membandingkan Data (Langkah Asas)
                st.write("### 🔍 Hasil Perbandingan")
                
                # Sistem semak adakah kedua-dua fail ada nama lajur (header) yang sama
                lajur_sama = list(set(df1.columns).intersection(set(df2.columns)))
                
                if lajur_sama:
                    st.info(f"Sistem mengesan lajur yang sama dalam kedua-dua fail iaitu: **{', '.join(lajur_sama)}**")
                    st.write("💡 *Nota: Memandangkan ada lajur yang sama, sistem boleh melakukan carian rekod yang bertindih (duplicate) nanti.*")
                else:
                    st.warning("Tiada nama lajur (header) yang sama dikesan. Sukar untuk sistem membandingkan data jika format jadual berbeza.")

            except Exception as e:
                st.error(f"Alamak, ada masalah semasa membaca fail: {e}")
        
        # --- LOGIK UNTUK WORD / PDF (Akan datang) ---
        else:
            st.info("Sistem bacaan untuk Word dan PDF akan ditambah di bahagian ini nanti!")
            
    else:
        st.warning("Sila muat naik kedua-dua fail terlebih dahulu.")
