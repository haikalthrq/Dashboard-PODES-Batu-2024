# Prompt untuk AI Developer

## Peran Anda:
Anda adalah seorang data scientist dan pengembang Python ahli dengan spesialisasi dalam membangun aplikasi data interaktif menggunakan Streamlit. Anda sangat teliti dalam merancang struktur aplikasi yang bersih dan mudah dikelola.

## Tujuan Utama:
Membangun sebuah aplikasi dashboard Streamlit fungsional sebagai prototipe untuk memvisualisasikan data Potensi Desa (Podes) 2024 Kota Batu. Aplikasi ini harus interaktif, informatif, dan sesuai dengan semua persyaratan yang diuraikan di bawah ini.

## 1. Konteks Proyek
Aplikasi ini ditujukan untuk Pemerintah Kota Batu sebagai alat bantu analisis dan pengambilan kebijakan. Data yang digunakan adalah hasil survei Podes 2024 yang sudah melalui proses pembersihan. Desain dashboard berfokus pada transparansi, perbandingan langsung antar desa, dan analisis berbasis data faktual tanpa menggunakan skor agregat.

## 2. Aset yang Disediakan
Anda akan bekerja dengan satu file data utama:

**data_podes_2024.json**: Ini adalah file JSON yang berisi array dari objek. Setiap objek mewakili satu desa dan memiliki struktur sebagai berikut:

- **Identitas**: `IDDESA`, `NAMA_KEC`, `NAMA_DESA`.
- **Data Kuantitatif**: `jumlah_tk`, `jumlah_sd`, `jumlah_smp`, `jumlah_sma`, `jumlah_rs`, `jumlah_puskesmas_inap`, `jumlah_puskesmas`.
- **Data Kualitatif (Label)**: `label_mitigasi_dini`, `label_mitigasi_alat`, `label_mitigasi_rambu`, `label_internet`, `label_sinyal_internet`, `label_angkutan_umum`.

## 3. Struktur File dan Folder Aplikasi
Untuk memastikan aplikasi mudah dikelola, gunakan struktur berikut:

dashboard-podes/
├── 📄 app.py # File utama aplikasi Streamlit
├── 📁 data/
│ └── 📄 data_podes_2024.json
├── 📁 modules/
│ ├── 📄 ui_components.py # Fungsi untuk membuat filter atau komponen UI
│ └── 📄 data_loader.py # Fungsi untuk memuat dan cache data
└── 📄 requirements.txt # Daftar library yang dibutuhkan (streamlit, pandas)


## 4. Persyaratan Fungsional Aplikasi

### A. Tata Letak (Layout)
Gunakan layout wide (`st.set_page_config(layout="wide")`).

Aplikasi harus memiliki **Sidebar** di sebelah kiri yang berfungsi sebagai Panel Kontrol utama untuk semua filter.

Area utama di sebelah kanan akan menampilkan **visualisasi data** yang berubah secara dinamis.

### B. Panel Kontrol (di dalam Sidebar)
Buat filter-filter berikut di dalam `st.sidebar`:

- **Filter Kategori Utama**: Sebuah selectbox untuk memilih kategori analisis:
  - Pendidikan
  - Kesehatan
  - Bencana & Lingkungan
  - Ekonomi & Konektivitas

- **Filter Indikator Dinamis**: Sebuah selectbox yang isinya berubah sesuai dengan Kategori Utama yang dipilih.
  - Jika Kategori = Pendidikan, maka pilihan indikatornya adalah `Jumlah TK`, `Jumlah SD`, dll.
  - Jika Kategori = Bencana & Lingkungan, maka pilihan indikatornya adalah `Sistem Peringatan Dini`, `Alat Keselamatan`, dll.

- **Filter Lokasi**:
  - Sebuah selectbox untuk memilih Kecamatan. Opsi harus menyertakan "Semua Kecamatan".
  - Sebuah multiselect untuk memilih Desa tertentu, yang opsinya disesuaikan berdasarkan Kecamatan yang dipilih.

### C. Area Visualisasi Utama
Area ini harus menampilkan konten yang relevan berdasarkan filter yang aktif.

- **Judul Dinamis**: Tampilkan judul yang mencerminkan filter yang sedang dipilih (misalnya, "Data Pendidikan di Kecamatan Batu").
  
- **Sistem Peringkat (Tanpa Skor)**:
  - Tampilkan data yang sudah difilter dalam bentuk tabel interaktif (`st.dataframe`).
  - Fitur ranking diwujudkan dengan kemampuan pengguna untuk mengurutkan (sort) tabel dengan mengklik judul kolom. Misalnya, mengklik kolom "jumlah_sma" akan mengurutkan desa dari yang memiliki SMA terbanyak ke yang paling sedikit. Ini adalah cara me-ranking tanpa skor.

- **Mode Perbandingan Desa**:
  - Di atas tabel, sediakan sebuah `st.multiselect` yang memungkinkan pengguna memilih dua atau lebih desa dari data yang ditampilkan.
  - Jika lebih dari satu desa dipilih, tampilkan sebuah bagian baru di bawahnya yang berisi perbandingan data side-by-side untuk desa-desa tersebut. Gunakan `st.metric` atau `st.bar_chart` untuk menampilkan perbandingan setiap indikator relevan.

## 5. Catatan Penting & Batasan

- **Tanpa Skor**: Aplikasi ini tidak boleh menghitung, menggunakan, atau menampilkan skor komposit apa pun. Semua analisis harus didasarkan pada data kuantitatif dan kualitatif yang ada di file JSON.
  
- **Tanpa Peta Heatmap**: Visualisasi peta dalam bentuk heatmap tidak akan diimplementasikan dalam prototipe Streamlit ini. Fitur peta adalah untuk pengembangan di tahap selanjutnya dan tidak termasuk dalam lingkup tugas ini.

- **Kode Berkualitas**: Tulis kode yang bersih, modular, dan beri komentar jika diperlukan. Gunakan fungsi-fungsi di dalam direktori `modules/` untuk menjaga `app.py` tetap rapi.

- **Caching Data**: Gunakan dekorator `@st.cache_data` untuk fungsi pemuatan data agar performa aplikasi cepat.