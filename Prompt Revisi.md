Revisi Utama

Ini adalah revisi untuk prompt sebelumnya. Fokus utama revisi ini adalah untuk memperkaya Halaman Dashboard Analisis dengan lebih banyak visualisasi dalam bentuk grafik dan diagram, mengurangi ketergantungan pada tampilan tabel saja. Semua spesifikasi lain dari prompt sebelumnya (struktur proyek, halaman muka, panel kontrol di sidebar, dll.) tetap berlaku.

Revisi Desain Area Konten Utama

Untuk menjaga agar tampilan tetap bersih dan tidak penuh sesak, Area Konten Utama pada halaman "Dashboard Analisis" akan menggunakan tata letak berbasis Tab. Gunakan st.tabs untuk membuat tiga bagian utama:

Tab 1: Ringkasan Visual (Visual Summary)

Tab 2: Data Rinci & Peringkat (Detailed Data & Ranking)

Tab 3: Perbandingan Desa (Village Comparison)

1. Rincian untuk Tab 1: Ringkasan Visual 📊

Tab ini adalah tempat untuk semua visualisasi grafik baru. Tampilan di tab ini harus sepenuhnya dinamis dan merespons filter di sidebar.

Judul Grafik Dinamis
Tampilkan judul yang jelas di atas setiap grafik, yang merefleksikan filter yang sedang aktif.
Contoh: st.subheader("Distribusi Status Peringatan Dini di Kecamatan Batu")

Logika Visualisasi Cerdas
Terapkan logika untuk menampilkan jenis grafik yang paling sesuai, tergantung pada tipe data dari indikator yang dipilih di sidebar:

Jika indikator bersifat KATEGORI

(misalnya, status_peringatan_dini, jenis_sinyal_internet):

Diagram Batang (Bar Chart): menghitung jumlah desa untuk setiap kategori.

Diagram Lingkaran (Pie Chart): ditampilkan di sebelahnya dengan st.columns, menunjukkan persentase distribusi.

Contoh Pertanyaan: “Berapa banyak desa yang memiliki status peringatan dini 'Ada' vs 'Tidak Ada'?”

Jika indikator bersifat KUANTITATIF/NUMERIK

(misalnya, jumlah_sma, jumlah_bts):

Histogram: menunjukkan distribusi nilai indikator.

Diagram Batang Horizontal (Horizontal Bar Chart): menampilkan 10 Desa dengan Nilai Tertinggi.

Contoh Pertanyaan: “Bagaimana sebaran jumlah SMA di seluruh desa?” dan “Desa mana saja yang masuk 10 besar pemilik SMA terbanyak?”

Rekomendasi Library
Gunakan Plotly Express atau Altair melalui st.plotly_chart atau st.altair_chart untuk membuat visualisasi ini karena mendukung kustomisasi dan interaktivitas lebih baik.

2. Rincian untuk Tab 2: Data Rinci & Peringkat 📋

Tab ini akan berisi tabel data interaktif (st.dataframe) seperti yang sudah dirancang sebelumnya.

Menjadi fitur utama untuk pengguna yang ingin melihat data mentah, melakukan eksplorasi mendalam, dan melakukan perankingan manual dengan mengklik judul kolom.

3. Rincian untuk Tab 3: Perbandingan Desa 🆚

Fitur ini aktif ketika pengguna memilih 2–3 desa di sidebar.

Gunakan Grouped Bar Chart (Diagram Batang Berkelompok) untuk membandingkan nilai kuantitatif antar desa.

Lebih efektif daripada hanya menampilkan angka metrik.

Contoh: membandingkan 2 desa pada kategori “Pendidikan” akan menghasilkan kelompok batang untuk “Jumlah TK”, “Jumlah SD”, dst., dengan warna berbeda untuk setiap desa.