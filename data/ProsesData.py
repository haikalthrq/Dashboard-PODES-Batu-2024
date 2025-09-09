import pandas as pd
import numpy as np

print("Memulai proses (tanpa skoring) dengan file 'cleaned_podes_data.csv'...")

try:
    # --- STAGE 1: Muat data yang sudah bersih ---
    cleaned_file_path = 'data/cleaned_podes_data.csv'
    df = pd.read_csv(cleaned_file_path)
    print(f"Tahap 1: File '{cleaned_file_path}' berhasil dimuat.")

    # --- STAGE 2: Proses data untuk dashboard ---
    # Ambil baris unik pertama untuk setiap desa
    df_unique = df.drop_duplicates(subset='IDDESA', keep='first').copy()
    print(f"Mengolah data untuk {len(df_unique)} desa unik...")

    # 2.1: Transformasi kode menjadi label (Bagian ini tetap penting)
    ada_tidak_map = {1: 'Ada', 2: 'Tidak Ada'}
    jenis_sinyal_map = {1: '5G', 2: '4G/LTE', 3: 'Lainnya', 4: 'Tidak Ada Internet'}

    df_unique['label_mitigasi_dini'] = df_unique['R604A'].map(ada_tidak_map).fillna('Data Tidak Tersedia')
    df_unique['label_mitigasi_alat'] = df_unique['R604C'].map(ada_tidak_map).fillna('Data Tidak Tersedia')
    df_unique['label_mitigasi_rambu'] = df_unique['R604D'].map(ada_tidak_map).fillna('Data Tidak Tersedia')
    df_unique['label_internet'] = df_unique['R1005A'].map(ada_tidak_map).fillna('Data Tidak Tersedia')
    df_unique['label_sinyal_internet'] = df_unique['R1005D'].map(jenis_sinyal_map).fillna('Data Tidak Tersedia')
    df_unique['label_angkutan_umum'] = df_unique['R1001C1'].map(ada_tidak_map).fillna('Data Tidak Tersedia')
    print("Tahap 2.1: Transformasi kode ke label selesai.")
    
    # 2.2: Bagian Perhitungan Skor dan Normalisasi DIHAPUS

    # 2.3: Finalisasi dan ekspor ke JSON
    # Pilih hanya kolom identitas, jumlah fasilitas (kuantitatif), dan label (kualitatif)
    kolom_final = [
        'IDDESA', 'NAMA_KEC', 'NAMA_DESA',
        'R701BK2', 'R701DK2', 'R701FK2', 'R701HK2',
        'R704AK2', 'R704CK2', 'R704DK2',
        'label_mitigasi_dini', 'label_mitigasi_alat', 'label_mitigasi_rambu',
        'label_internet', 'label_sinyal_internet', 'label_angkutan_umum'
    ]
    df_final = df_unique[kolom_final]
    df_final = df_final.rename(columns={
        'R701BK2': 'jumlah_tk', 'R701DK2': 'jumlah_sd', 'R701FK2': 'jumlah_smp', 'R701HK2': 'jumlah_sma',
        'R704AK2': 'jumlah_rs', 'R704CK2': 'jumlah_puskesmas_inap', 'R704DK2': 'jumlah_puskesmas',
    })
    print("Tahap 2.2: Finalisasi kolom (tanpa skor) selesai.")

    output_path = 'data_untuk_dashboard.json'
    df_final.to_json(output_path, orient='records', indent=4)
    print(f"\nPROSES SELESAI! File '{output_path}' (tanpa skor) telah berhasil dibuat.")

except FileNotFoundError:
    print(f"ERROR: File '{cleaned_file_path}' tidak ditemukan. Pastikan skrip ini ada di folder yang sama dengan data Anda.")
except Exception as e:
    print(f"Terjadi error: {e}")