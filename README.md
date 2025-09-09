# 🏘️ Dashboard Podes 2024 - Kota Batu

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

Aplikasi dashboard interaktif untuk memvisualisasikan data **Potensi Desa (Podes) 2024** Kota Batu. Dashboard ini dirancang khusus untuk mendukung Pemerintah Kota Batu dalam analisis data dan pengambilan kebijakan berbasis data faktual.

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Screenshot](#-screenshot)
- [Instalasi](#-instalasi)
- [Cara Penggunaan](#-cara-penggunaan)
- [Struktur Data](#-struktur-data)
- [Struktur Proyek](#-struktur-proyek)
- [Teknologi](#-teknologi)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)

## ✨ Fitur Utama

### 🎛️ Panel Kontrol Dinamis
- **Filter Kategori**: Pendidikan, Kesehatan, Bencana & Lingkungan, Ekonomi & Konektivitas
- **Filter Indikator**: Dinamis berdasarkan kategori yang dipilih
- **Filter Lokasi**: Pilihan kecamatan dan desa yang dapat dikustomisasi

### 📊 Visualisasi Data
- **Tabel Interaktif**: Ranking otomatis dengan klik header kolom
- **Mode Perbandingan**: Perbandingan side-by-side antar desa
- **Insight Statistik**: Analisis mendalam dengan grafik interaktif
- **Responsif**: Layout yang optimal untuk berbagai ukuran layar

### 🔍 Analisis Mendalam
- Statistik deskriptif (rata-rata, median, maksimum, minimum)
- Top 5 ranking untuk setiap indikator
- Distribusi data untuk variabel kategorikal
- Grafik perbandingan yang dapat dikustomisasi

## 📸 Screenshot

> *Screenshot akan ditambahkan setelah deployment*

## 🚀 Instalasi

### Prasyarat
- Python 3.8 atau lebih baru
- pip (Python package installer)

### Langkah Instalasi

1. **Clone repository**
   ```bash
   git clone https://github.com/your-username/dashboard-podes-2024.git
   cd dashboard-podes-2024
   ```

2. **Buat virtual environment (opsional tapi disarankan)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Pastikan file data tersedia**
   - File `data/data_podes_2024.json` harus tersedia di direktori proyek
   - Struktur data harus sesuai dengan format yang dijelaskan di bagian [Struktur Data](#-struktur-data)

5. **Jalankan aplikasi**
   ```bash
   streamlit run app.py
   ```

6. **Buka browser**
   - Aplikasi akan tersedia di `http://localhost:8501`

## 📖 Cara Penggunaan

### 1. Memilih Kategori Analisis
- Gunakan dropdown **"Kategori Analisis"** di sidebar
- Pilih dari: Pendidikan, Kesehatan, Bencana & Lingkungan, atau Ekonomi & Konektivitas

### 2. Memilih Indikator Spesifik
- Dropdown **"Indikator"** akan berubah sesuai kategori yang dipilih
- Contoh: Jika memilih "Pendidikan", akan muncul opsi TK, SD, SMP, SMA

### 3. Filter Lokasi
- **Kecamatan**: Pilih kecamatan tertentu atau "Semua Kecamatan"
- **Desa**: Pilih desa spesifik (opsional, multiselect)

### 4. Menggunakan Fitur Ranking
- Klik header kolom pada tabel untuk mengurutkan data
- Ranking otomatis berdasarkan nilai tertinggi/terendah

### 5. Mode Perbandingan Desa
- Pindah ke tab **"Perbandingan Desa"**
- Pilih 2 atau lebih desa untuk perbandingan
- Lihat metrics dan grafik perbandingan

### 6. Analisis Insight
- Tab **"Insight & Statistik"** menyediakan:
  - Statistik deskriptif
  - Top 5 ranking
  - Distribusi data

## 📊 Struktur Data

Data Podes 2024 menggunakan format JSON dengan struktur berikut:

```json
{
  "IDDESA": 3579010001,
  "NAMA_KEC": "BATU",
  "NAMA_DESA": "ORO-ORO OMBO",
  "jumlah_tk": 0,
  "jumlah_sd": 3,
  "jumlah_smp": 0,
  "jumlah_sma": 0,
  "jumlah_rs": 0,
  "jumlah_puskesmas_inap": 0,
  "jumlah_puskesmas": 0,
  "label_mitigasi_dini": "Ada",
  "label_mitigasi_alat": "Ada",
  "label_mitigasi_rambu": "Ada",
  "label_sinyal_internet": "5G/4G",
  "label_angkutan_umum": "Ada"
}
```

### Kategori Data:

#### 📚 Pendidikan
- `jumlah_tk`: Jumlah Taman Kanak-kanak
- `jumlah_sd`: Jumlah Sekolah Dasar
- `jumlah_smp`: Jumlah Sekolah Menengah Pertama
- `jumlah_sma`: Jumlah Sekolah Menengah Atas

#### 🏥 Kesehatan
- `jumlah_rs`: Jumlah Rumah Sakit
- `jumlah_puskesmas_inap`: Jumlah Puskesmas Rawat Inap
- `jumlah_puskesmas`: Jumlah Puskesmas

#### ⚠️ Bencana & Lingkungan
- `label_mitigasi_dini`: Sistem Peringatan Dini
- `label_mitigasi_alat`: Alat Keselamatan
- `label_mitigasi_rambu`: Rambu Keselamatan

#### 💼 Ekonomi & Konektivitas
- `label_sinyal_internet`: Kualitas Sinyal Internet
- `label_angkutan_umum`: Ketersediaan Angkutan Umum

## 🗂️ Struktur Proyek

```
dashboard-podes/
├── 📄 app.py                    # File utama aplikasi Streamlit
├── 📄 requirements.txt          # Dependencies Python
├── 📄 README.md                 # Dokumentasi proyek
├── 📁 data/
│   └── 📄 data_podes_2024.json  # Data Podes 2024
├── 📁 modules/
│   ├── 📄 __init__.py           # Python package init
│   ├── 📄 data_loader.py        # Modul pemuatan dan cache data
│   └── 📄 ui_components.py      # Komponen UI dan visualisasi
└── 📁 screenshots/              # Screenshot aplikasi (opsional)
```

## 🛠️ Teknologi

- **[Streamlit](https://streamlit.io/)** - Framework aplikasi web untuk data science
- **[Pandas](https://pandas.pydata.org/)** - Manipulasi dan analisis data
- **[Plotly](https://plotly.com/)** - Visualisasi data interaktif
- **Python 3.8+** - Bahasa pemrograman

## 📋 Requirements

```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
```

## 🎯 Fitur yang Akan Datang

- [ ] Export data ke Excel/CSV
- [ ] Visualisasi peta heatmap
- [ ] Dashboard perbandingan tahun ke tahun
- [ ] API endpoints untuk integrasi
- [ ] Notifikasi otomatis untuk data baru
- [ ] Mode dark theme

## 🤝 Kontribusi

Kontribusi sangat diterima! Untuk berkontribusi:

1. Fork repository ini
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 Catatan Penting

- **Tanpa Skor Komposit**: Dashboard ini tidak menggunakan skor gabungan, semua analisis berdasarkan data mentah
- **Fokus Transparansi**: Semua data ditampilkan apa adanya untuk transparansi maksimal
- **Optimasi Performa**: Menggunakan caching Streamlit untuk loading data yang cepat

## 📞 Kontak

**Tim Pengembang PKL BPS Batu**
- 📧 Email: [email-kontak]
- 🏛️ Instansi: BPS Kota Batu
- 📍 Lokasi: Kota Batu, Jawa Timur

## 📄 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE) - lihat file LICENSE untuk detail.

---

<div align="center">

**🏘️ Dibuat dengan ❤️ untuk Kota Batu 🏘️**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-streamlit-app-url.com)

</div>

## 🚀 Quick Start

Untuk memulai dengan cepat:

```bash
# Clone dan setup
git clone https://github.com/your-username/dashboard-podes-2024.git
cd dashboard-podes-2024
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run app.py
```

Kemudian buka browser dan kunjungi `http://localhost:8501` untuk melihat dashboard!

---

> **Catatan**: Pastikan file data Podes 2024 sudah tersedia sebelum menjalankan aplikasi. Hubungi tim pengembang jika memerlukan akses ke data.
