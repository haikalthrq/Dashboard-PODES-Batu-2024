# Prompt untuk AI Developer

## Peran Anda:
Anda adalah seorang Pengembang Python ahli dengan spesialisasi dalam pembuatan aplikasi data interaktif menggunakan Streamlit dan Pandas. Anda memiliki pemahaman mendalam tentang prinsip-prinsip UI/UX untuk menciptakan dasbor yang tidak hanya fungsional, tetapi juga profesional, intuitif, dan mudah digunakan oleh para pemangku kepentingan di level pemerintahan.

## Tujuan Proyek:
Tugas Anda adalah membangun sebuah prototipe aplikasi web fungsional dan rapi menggunakan Streamlit. Aplikasi ini berfungsi sebagai dasbor interaktif untuk menganalisis Data Potensi Desa (Podes) 2024 untuk wilayah Kota Batu, yang akan digunakan sebagai alat bantu pengambilan kebijakan berbasis data.

## Struktur Proyek
Untuk memastikan kemudahan pemeliharaan dan skalabilitas, gunakan struktur file dan folder modular berikut:

dashboard_podes_batu/
├── 📄 app.py # Skrip utama yang mengatur halaman
├── 📁 data/
│ └── 📄 data_podes_2024.json
├── 📁 modules/
│ ├── 📄 data_loader.py # Fungsi untuk memuat dan cache data
│ ├── 📄 ui_components.py # Fungsi untuk membangun elemen UI (sidebar, judul, kartu KPI)
│ └── 📄 analysis.py # Fungsi untuk analisis (perbandingan, filtering)
├── 📁 pages/
│ └── 📄 1_Dashboard_Analisis.py # Halaman utama dashboard
└── 📄 requirements.txt # Daftar library (streamlit, pandas)


## Sumber Data
Gunakan file `data/data_podes_2024.json` sebagai satu-satunya sumber data. Strukturnya adalah sebuah array JSON di mana setiap objek mewakili satu desa. Semua kunci dan nilai kategori di dalamnya sudah deskriptif dan siap pakai.

## Desain & Alur Pengguna (UI/UX)
Aplikasi ini akan berjalan sebagai aplikasi multi-halaman Streamlit.

### 1. Halaman Muka (`app.py`)
Ini adalah landing page yang profesional dan rapi.

**Layout**: Gunakan `st.columns` untuk menciptakan tata letak yang seimbang (misalnya, teks di satu sisi, gambar/logo di sisi lain).

**Konten**:

- **Judul Utama**: "Dashboard Interaktif Potensi Desa Kota Batu".
- **Subjudul**: "Analisis Data Podes 2024 untuk Perencanaan Berbasis Bukti".
- **Deskripsi**: Tampilkan teks ringkas yang menjelaskan tujuan dasbor, sumber data (BPS), dan manfaatnya. Gunakan bahasa yang formal dan profesional.
- **Call to Action**: Sediakan sebuah tombol `st.button` yang jelas, misalnya [Jelajahi Dashboard], yang akan mengarahkan pengguna ke halaman "Dashboard Analisis".

### 2. Halaman Dashboard Analisis (`pages/1_Dashboard_Analisis.py`)
Ini adalah halaman inti aplikasi.

#### A. Panel Kontrol (Sidebar)
Gunakan `st.sidebar` untuk semua kontrol interaktif:

- **Filter Kategori Utama**: Sebuah `st.selectbox` untuk memilih salah satu dari empat kategori utama:
  - Pendidikan
  - Kesehatan
  - Infrastruktur & Konektivitas
  - Lingkungan & Kebencanaan

- **Filter Indikator Spesifik**: Sebuah `st.selectbox` yang isinya berubah secara dinamis berdasarkan pilihan Kategori Utama. Daftar indikator untuk setiap kategori harus sesuai dengan yang telah didefinisikan sebelumnya (contoh: jika Kategori="Pendidikan", maka Indikator="Jumlah TK", "Jumlah SD", dst.).

- **Filter Lokasi**:
  - `st.selectbox` untuk Kecamatan, dengan opsi "Semua Kecamatan".
  - `st.multiselect` untuk Desa/Kelurahan, memungkinkan pengguna memilih beberapa desa sekaligus untuk fitur perbandingan.

- **Tombol Reset**: Sebuah `st.button("Reset Filter")` untuk mengembalikan semua pilihan ke kondisi awal.

#### B. Area Konten Utama
- **Judul Dinamis**: Tampilkan judul yang berubah sesuai filter, misalnya: `st.header("Analisis Pendidikan: Jumlah SMA di Kecamatan Batu")`.

- **Kartu KPI Agregat**: Sebelum tabel, tampilkan 3-4 ringkasan data teratas menggunakan `st.columns` dan `st.metric`.
  - Jika indikatornya kuantitatif (misal: jumlah_sma), tampilkan: Total se-Kota Batu, Rata-rata per Desa, dan Desa dengan Nilai Tertinggi.
  - Jika indikatornya kualitatif (misal: status_peringatan_dini), tampilkan: Jumlah Desa dengan 'Ada', Jumlah Desa dengan 'Tidak Ada', dan Persentase Desa dengan 'Ada'.

- **Tabel Peringkat Interaktif**:
  - Tampilkan `st.dataframe` yang berisi data desa yang telah difilter.
  - **Sistem Peringkat**: Pengguna dapat mengklik judul kolom pada tabel untuk mengurutkan data (ascending/descending). Inilah yang berfungsi sebagai sistem perankingan manual berbasis indikator tunggal, sesuai dengan permintaan.

- **Fitur Perbandingan Desa**:
  - Fitur ini aktif jika pengguna memilih 2 atau 3 desa di filter multiselect Desa.
  - Tampilkan sub-header "Perbandingan Desa".
  - Gunakan `st.columns` untuk menampilkan data dari desa-desa yang dipilih secara berdampingan.
  - Sajikan perbandingan menggunakan `st.metric` atau `st.bar_chart` sederhana untuk setiap indikator relevan dalam kategori yang dipilih.