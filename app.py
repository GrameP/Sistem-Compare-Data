import streamlit as st
import pandas as pd
import pypdf
import base64
import os

# Tetapan muka surat web
st.set_page_config(page_title="Sistem Banding BAJPM", layout="wide", page_icon="🛡️")

# Fungsi untuk baca gambar Jata Negara dari dalam PC (Kalis Firewall)
def dapatkan_base64_gambar(nama_fail):
    if os.path.exists(nama_fail):
        with open(nama_fail, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

# Tarik fail 'logo.png' dari folder yang sama
logo_base64 = dapatkan_base64_gambar("logo.png")
sumber_gambar = f"data:image/png;base64,{logo_base64}" if logo_base64 else ""

# Kalau terlupa letak logo, sistem akan bagi amaran kecil
tag_gambar = f'<img src="{sumber_gambar}" class="jata-negara">' if logo_base64 else '<div style="color:#FCA5A5; margin-bottom:15px; border: 1px dashed red; padding: 10px;">[Sila letak fail <b>logo.png</b> di dalam folder Sistem Banding]</div>'

# ==========================================
# BAHAGIAN 1 & 2: CSS DAN HEADER (JATA NEGARA)
# ==========================================
st.markdown(f"""
<style>
    /* TUKAR WARNA BACKGROUND KESELURUHAN (DARK ROYAL BLUE) */
    .stApp {{
        background-color: #05005D; /* Kod warna rasmi dari gambar kau */
    }}
    
    /* Buat bar atas jadi transparent supaya warna biru tak terpotong */
    [data-testid="stHeader"] {{
        background-color: transparent;
    }}

    /* CSS Untuk Tajuk & Logo */
    .header-container {{ display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin-bottom: 2rem; }}
    .jata-negara {{ width: 140px; margin-bottom: 15px; drop-shadow: 0px 4px 6px rgba(0,0,0,0.5); }}
    .tajuk-utama {{ font-size: 2.2rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; color: #FFFFFF; }}
    .tajuk-sub {{ font-size: 1.2rem; font-weight: 400; letter-spacing: 2px; color: #FBBF24; margin-bottom: 20px; }}
    
    /* CSS Untuk Footer */
    .footer-container {{ text-align: center; margin-top: 80px; padding-top: 20px; border-top: 1px solid #334155; color: #94A3B8; font-size: 0.9rem; line-height: 1.5; }}
</style>

<div class="header-container">
    {tag_gambar}
    <div class="tajuk-utama">SISTEM PERBANDINGAN DOKUMEN</div>
    <div class="tajuk-sub">SEKSYEN BAYARAN BAJPM</div>
</div>
""", unsafe_allow_html=True)
st.write("---")

# ==========================================
# BAHAGIAN 3: SISTEM PERBANDINGAN
# ==========================================
col1, col2 = st.columns(2)
with col1:
    st.subheader("Fail Pertama (A)")
    file_1 = st.file_uploader("Muat naik Fail A", type=["pdf", "docx", "xlsx", "csv"], key="file1")
with col2:
    st.subheader("Fail Kedua (B)")
    file_2 = st.file_uploader("Muat naik Fail B", type=["pdf", "docx", "xlsx", "csv"], key="file2")

if file_1 and file_2:
    nama_fail_1 = file_1.name.lower()
    nama_fail_2 = file_2.name.lower()
    
    # --- LOGIK EXCEL/CSV ---
    if nama_fail_1.endswith(('.xlsx', '.csv')) and nama_fail_2.endswith(('.xlsx', '.csv')):
        try:
            df1 = pd.read_csv(file_1) if nama_fail_1.endswith('.csv') else pd.read_excel(file_1)
            df2 = pd.read_csv(file_2) if nama_fail_2.endswith('.csv') else pd.read_excel(file_2)

            st.success("Kedua-dua fail Excel berjaya dibaca!")
            st.write("### 📊 Paparan Data Asas")
            colA, colB = st.columns(2)
            with colA: st.dataframe(df1, height=200)
            with colB: st.dataframe(df2, height=200)
            
            st.write("### ⚙️ Tetapan Perbandingan")
            col_pilih_A, col_pilih_B = st.columns(2)
            with col_pilih_A: pilihan_A = st.selectbox("Pilih lajur untuk Fail A:", df1.columns)
            with col_pilih_B: pilihan_B = st.selectbox("Pilih lajur untuk Fail B:", df2.columns)

            st.write("### 🎯 Hasil Perbandingan")
            data_A = df1[pilihan_A].astype(str).dropna().tolist()
            data_B = df2[pilihan_B].astype(str).dropna().tolist()
            persamaan = set(data_A).intersection(set(data_B))
            
            if persamaan:
                st.success(f"Terdapat {len(persamaan)} rekod yang SAMA ditemui!")
                df_hasil = pd.DataFrame(list(persamaan), columns=["Data Sama"])
                st.dataframe(df_hasil)
            else:
                st.warning("Tiada sebarang persamaan data ditemui.")
        except Exception as e:
            st.error(f"Ralat semasa memproses fail Excel: {e}")

    # --- LOGIK PDF ---
    elif nama_fail_1.endswith('.pdf') and nama_fail_2.endswith('.pdf'):
        try:
            def baca_pdf(fail_pdf):
                pembaca = pypdf.PdfReader(fail_pdf)
                teks_penuh = ""
                for muka_surat in pembaca.pages:
                    teks = muka_surat.extract_text()
                    if teks:
                        teks_penuh += teks + "\n"
                return teks_penuh

            teks_A = baca_pdf(file_1)
            teks_B = baca_pdf(file_2)
            
            st.success("Teks PDF berjaya diekstrak!")
            st.divider()

            st.write("### 📄 Paparan Teks PDF")
            col_pdf1, col_pdf2 = st.columns(2)
            with col_pdf1: st.text_area("Kandungan Fail A (Mentah)", teks_A, height=250)
            with col_pdf2: st.text_area("Kandungan Fail B (Mentah)", teks_B, height=250)
            
            st.divider()
            st.write("### 🎯 Hasil Perbandingan Barisan/Ayat")
            
            barisan_A = set([ayat.strip() for ayat in teks_A.split('\n') if ayat.strip()])
            barisan_B = set([ayat.strip() for ayat in teks_B.split('\n') if ayat.strip()])
            ayat_sama = barisan_A.intersection(barisan_B)
            
            if ayat_sama:
                st.success(f"Terdapat {len(ayat_sama)} barisan maklumat yang SAMA dikesan!")
                df_hasil_pdf = pd.DataFrame(list(ayat_sama), columns=["Maklumat/Ayat Yang Sama"])
                st.dataframe(df_hasil_pdf, use_container_width=True)
            else:
                st.warning("Tiada sebarang persamaan data yang tepat ditemui.")

        except Exception as e:
            st.error(f"Ralat semasa memproses fail PDF: {e}")
            
    else:
        st.error("Sila pastikan kedua-dua fail adalah format yang sama (Cth: Excel dengan Excel, atau PDF dengan PDF).")

# ==========================================
# BAHAGIAN 4: FOOTER (KREDIT NAMA KAU)
# ==========================================
st.markdown("""
<div class="footer-container">
    <strong>Dihasilkan Oleh:</strong><br>
    Nor Azwan Bin Alias<br>
    Seksyen Bayaran BAJPM<br>
    <br>
    &copy; 2026 Sistem Digital Seksyen Bayaran BAJPM
</div>
""", unsafe_allow_html=True)
