# Dokumentasi Data: Dashboard Potensi Desa

Dokumen ini menjelaskan metodologi di balik pembuatan file **data_untuk_dashboard.json**. Tujuannya adalah untuk memberikan transparansi mengenai asal-usul setiap label (data teks) dan data kuantitatif (jumlah fasilitas) yang digunakan dalam visualisasi.

Sesuai keputusan desain terbaru, sistem skor telah dihapus untuk memungkinkan analisis dan identifikasi fasilitas secara individual dan lebih transparan.

---

## Struktur Data Final

File **data_untuk_dashboard.json** berisi sebuah array dari objek-objek. Setiap objek mewakili satu desa dan kini hanya berisi tiga jenis informasi utama:

1. **Identitas Desa**: `IDDESA`, `NAMA_KEC`, `NAMA_DESA`.

2. **Data Kuantitatif**: Jumlah faktual setiap fasilitas (contoh: `jumlah_tk`, `jumlah_sd`, `jumlah_puskesmas`).

3. **Data Kualitatif (Label)**: Informasi deskriptif yang sudah diterjemahkan dari kode (contoh: `label_internet`, `label_mitigasi_dini`).

---

## Metodologi Label

Label dibuat untuk menerjemahkan data kode numerik dari kuesioner menjadi teks yang bisa dibaca manusia. Proses ini menggunakan metode *mapping*. Jika ada data asli yang tidak sesuai dengan kode yang didefinisikan, labelnya akan menjadi **"Data Tidak Tersedia"**.

| Kolom Asli | Nilai Asli (Kode) | Kolom Baru (Label) | Nilai Baru (Teks) |
|------------|-------------------|--------------------|--------------------|
| R604A | 1, 2 | label_mitigasi_dini | 'Ada', 'Tidak Ada' |
| R604C | 1, 2 | label_mitigasi_alat | 'Ada', 'Tidak Ada' |
| R604D | 1, 2 | label_mitigasi_rambu | 'Ada', 'Tidak Ada' |
| R1005A | 1, 2 | label_internet | 'Ada', 'Tidak Ada' |
| R1001C1 | 1, 2 | label_angkutan_umum | 'Ada', 'Tidak Ada' |
| R1005D | 1, 2, 3, 4 | label_sinyal_internet | '5G', '4G/LTE', 'Lainnya', 'Tidak Ada' |

---

## Export to Sheets

---

## Penggunaan Data di Dashboard

Tanpa adanya skor agregat, analisis di dashboard akan berfokus pada metode yang lebih langsung dan transparan:

### Filtering & Pemetaan Langsung
Pengguna dapat memfilter dan melihat persebaran fasilitas secara langsung di peta heatmap. Contohnya, pengguna bisa memilih untuk menampilkan semua desa yang memiliki `jumlah_sma > 0`.

### Perbandingan Langsung
Fitur "Bandingkan Desa" menjadi metode utama untuk analisis. Fitur ini akan menampilkan jumlah fasilitas dari desa-desa yang dipilih secara berdampingan, memungkinkan perbandingan data faktual.

### Analisis Mandiri
Pengguna didorong untuk menarik kesimpulan sendiri berdasarkan data kuantitatif yang disajikan, bukan berdasarkan skor yang sudah diabstraksikan.