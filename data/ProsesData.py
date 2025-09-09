import pandas as pd
import numpy as np

print("Memulai proses konversi dan mapping untuk SEMUA variabel...")

try:
    # --- TAHAP 1: MUAT DATA ---
    cleaned_file_path = 'data/cleaned_podes_data.csv'
    df = pd.read_csv(cleaned_file_path)
    print(f"-> File '{cleaned_file_path}' berhasil dimuat.")

    # --- TAHAP 2: PERSIAPAN DATA ---
    # Mengatasi duplikasi data
    df_unique = df.drop_duplicates(subset='IDDESA', keep='first').copy()
    print(f"-> Data unik untuk {len(df_unique)} desa telah disiapkan.")

    # --- TAHAP 3: KAMUS PEMETAAN LENGKAP ---
    # Berdasarkan analisis kuesioner, berikut kamus untuk semua variabel kategori
    map_ada_tidak = {1: 'Ada', 2: 'Tidak Ada'}
    map_ada_tidak_digunakan = {1: 'Ada, digunakan', 2: 'Ada, tidak digunakan', 3: 'Tidak ada'}
    map_listrik = {1: 'Ya, sebagian besar', 2: 'Ya, sebagian kecil', 3: 'Tidak ada'}
    map_penerangan_jalan = {1: 'Ada, sebagian besar', 2: 'Ada, sebagian kecil', 3: 'Tidak Ada'}
    map_perolehan_kayu = {1: 'Membeli', 2: 'Dari hutan', 3: 'Dari luar hutan', 4: 'Lainnya'}
    map_pemilahan_sampah = {1: 'Semua Keluarga', 2: 'Sebagian Besar Keluarga', 3: 'Sebagian Kecil Keluarga', 4: 'Tidak Ada'}
    map_lokasi_sumber_pencemaran_air = {1: 'Dalam desa/kelurahan ini', 2: 'Luar desa/kelurahan ini', 3: 'Luar dan dalam desa/kelurahan ini'}
    map_pengolahan_daur_ulang = {1: 'Ada, sebagian warga terlibat', 2: 'Ada, warga tidak terlibat', 3: 'Tidak ada kegiatan'}
    map_ya_tidak = {1: 'Ya', 2: 'Tidak'}
    map_status_aktif = {1: 'Ada, aktif', 2: 'Ada, tidak aktif', 3: 'Tidak ada'}
    map_kejadian_bencana = {1: 'Ada', 2: 'Tidak ada'}
    map_simulasi_bencana = {1: 'Sebagian Besar Warga', 2: 'Sebagian Kecil Warga', 3: 'Tidak Ada'}
    map_kekuatan_sinyal = {1: 'Sangat Kuat', 2: 'Kuat', 3: 'Lemah', 4: 'Tidak Ada Sinyal'}
    map_sinyal_internet = {1: '5G/4G/LTE', 2: '3G/H/H+/EVDO ', 3: '2,5G/E/GPRS', 4: 'Tidak Ada Internet'}
    
    print("-> Kamus untuk mapping nilai kategori telah dibuat.")

    # --- TAHAP 4: MEMBUAT DATA FRAME BARU YANG BERSIH ---
    df_final = pd.DataFrame()

    # Salin kolom identitas
    df_final['id_desa'] = df_unique['IDDESA']
    df_final['nama_kecamatan'] = df_unique['NAMA_KEC']
    df_final['nama_desa'] = df_unique['NAMA_DESA']

    # Proses semua kolom dari cleaned_podes_data.csv
    # Kolom kontinu (hanya rename)
    df_final['jumlah_keluarga_pengguna_kayu_bakar'] = df_unique['R503A10']
    df_final['jumlah_tk'] = df_unique['R701BK2']
    df_final['jumlah_sd'] = df_unique['R701DK2']
    df_final['jumlah_smp'] = df_unique['R701FK2']
    df_final['jumlah_sma'] = df_unique['R701HK2']
    df_final['jumlah_rs'] = df_unique['R704AK2']
    df_final['jumlah_puskesmas_inap'] = df_unique['R704CK2']
    df_final['jumlah_puskesmas'] = df_unique['R704DK2']
    df_final['jumlah_bts'] = df_unique['R1005A']

    # Kolom kategori (rename dan mapping nilai)
    df_final['status_penerangan_jalan_surya'] = df_unique['R502A'].map(map_ada_tidak).fillna('Tidak Terdefinisi')
    df_final['status_penerangan_jalan_utama'] = df_unique['R502B'].map(map_penerangan_jalan).fillna('Tidak Terdefinisi')
    df_final['cara_perolehan_kayu_bakar'] = df_unique['R503C'].map(map_perolehan_kayu).fillna('Tidak Terdefinisi')
    df_final['status_buang_sampah_dibakar'] = df_unique['R504A2'].map(map_ada_tidak).fillna('Tidak Terdefinisi')
    df_final['status_tps'] = df_unique['R504C'].map(map_ada_tidak).fillna('Tidak Terdefinisi')
    df_final['status_tps3r'] = df_unique['R504D'].map(map_ada_tidak_digunakan).fillna('Tidak Terdefinisi')
    df_final['status_dilakukan_pemilahan_sampah'] = df_unique['R504F1'].map(map_ada_tidak).fillna('Tidak Terdefinisi')
    df_final['kebiasaan_pemilahan_sampah'] = df_unique['R505'].map(map_pemilahan_sampah).fillna('Tidak Terdefinisi')
    df_final['permukiman_bantaran_sungai'] = df_unique['R511C1'].map(map_ya_tidak).fillna('Tidak Terdefinisi')
    df_final['sumber_pencemaran_air_dari_pabrik'] = df_unique['R511C2A'].map(map_ya_tidak).fillna('Tidak Terdefinisi')
    df_final['sumber_pencemaran_air_dari_rumah'] = df_unique['R511C2B'].map(map_ya_tidak).fillna('Tidak Terdefinisi')
    df_final['sumber_pencemaran_air_dari_lainnya'] = df_unique['R511C2C'].map(map_ya_tidak).fillna('Tidak Terdefinisi')
    df_final['lokasi_sumber_pencemaran_air'] = df_unique['R511C3'].map(map_lokasi_sumber_pencemaran_air).fillna('Tidak Terdefinisi')  
    df_final['warga_terlibat_olah_sampah'] = df_unique['R515B'].map(map_pengolahan_daur_ulang).fillna('Tidak Terdefinisi')
    df_final['komunitas_lingkungan'] = df_unique['R516'].map(map_status_aktif).fillna('Tidak Terdefinisi')
    df_final['kebiasaan_bakar_lahan'] = df_unique['R517'].map(map_ada_tidak).fillna('Tidak Terdefinisi')
    df_final['kejadian_tanah_longsor'] = df_unique['R601AK2'].map(map_kejadian_bencana).fillna('Tidak Terdefinisi')
    df_final['kejadian_banjir'] = df_unique['R601BK2'].map(map_kejadian_bencana).fillna('Tidak Terdefinisi')
    df_final['kejadian_gempa'] = df_unique['R601DK2'].map(map_kejadian_bencana).fillna('Tidak Terdefinisi')
    df_final['status_peringatan_dini'] = df_unique['R604A'].map(map_ada_tidak).fillna('Tidak Terdefinisi')
    df_final['status_alat_keselamatan'] = df_unique['R604C'].map(map_ada_tidak).fillna('Tidak Terdefinisi')
    df_final['status_rambu_evakuasi'] = df_unique['R604D'].map(map_ada_tidak).fillna('Tidak Terdefinisi')
    df_final['partisipasi_simulasi_bencana'] = df_unique['R6061'].map(map_simulasi_bencana).fillna('Tidak Terdefinisi')
    df_final['partisipasi_gladi_siaga_bencana'] = df_unique['R6062'].map(map_simulasi_bencana).fillna('Tidak Terdefinisi')
    df_final['kekuatan_sinyal'] = df_unique['R1005C'].map(map_kekuatan_sinyal).fillna('Tidak Terdefinisi')
    df_final['jenis_sinyal_internet'] = df_unique['R1005D'].map(map_sinyal_internet).fillna('Tidak Terdefinisi')
    
    print("-> Semua variabel dari 'cleaned_podes_data.csv' telah diproses.")

    # --- TAHAP 5: EKSPOR KE JSON ---
    output_path = 'data_podes_2024_all_variables_mapped.json'
    # Menggunakan force_ascii=False agar karakter non-latin tersimpan dengan benar
    df_final.to_json(output_path, orient='records', indent=4, force_ascii=False)
    print(f"\nPROSES SELESAI! File '{output_path}' yang memuat semua variabel telah berhasil dibuat.")
    
except FileNotFoundError:
    print(f"ERROR: File '{cleaned_file_path}' tidak ditemukan. Pastikan skrip ini ada di folder yang sama dengan data Anda.")
except KeyError as e:
    print(f"ERROR: Terjadi kesalahan nama kolom: {e}. Pastikan file '{cleaned_file_path}' memiliki semua kolom yang dibutuhkan.")
except Exception as e:
    print(f"Terjadi error: {e}")