# RoboCamp for Student

Proyek ini untuk mendeteksi objek secara real-time menggunakan webcam, file video, atau gambar, dengan model YOLO (You Only Look Once).

## Tugas yang Telah Selesai

1. **Object Detection**:
   - ✅ Bouy Merah
   - ✅ Bouy Hijau
   - ✅ Obstacle
   - ✅ Bounding Box
   - ✅ Class Label

2. **Midpoint Navigation**:
   - ✅ Hitung midpoint antara bouy merah dan hijau
   - ✅ Tampilkan sebagai acuan arah gerak

3. **Autonomous Decision**:
   - ✅ LEFT: Midpoint di kiri
   - ✅ RIGHT: Midpoint di kanan
   - ✅ FORWARD: Midpoint di tengah
   - ✅ STOP: Ada obstacle di depan

4. **Obstacle Avoidance (Bonus)**:
   - ✅ Mendeteksi obstacle di depan
   - ✅ Menentukan arah penghindaran (kiri/kanan)
   - ✅ Menjaga kapal menuju midpoint setelah obstacle

## Struktur File Proyek

```
robocamp_for_student/
├── assets/                    # Folder untuk gambar bouy
├── models/                    # Folder untuk video bouy
├── main.py                    # Menu utama
├── main_webcame.py            # Webcam - Deteksi semua benda
├── main_video.py              # Video - Tugas 1-4 lengkap
├── main_image.py              # Gambar - Deteksi bouy di gambar
├── bola.pt                    # Model YOLO custom
├── yolov8n.pt                 # Model YOLO standar
├── requirements.txt           # Daftar dependensi
└── README.md                  # Dokumentasi proyek
```

## Instalasi

1. Pastikan kamu sudah install Python di komputer kamu.
2. Buka terminal atau command prompt.
3. Pindah ke direktori proyek ini:
   ```
   cd c:\robocamp\robocamp_for_student
   ```
4. Install semua dependensi yang dibutuhkan:
   ```
   pip install -r requirements.txt
   ```

## Cara Pakai

### 1. Menu Utama (main.py)

Jalankan program utama untuk memilih fitur:
```
python main.py
```

Pilih opsi yang diinginkan:
- **1**: Webcam - Deteksi semua benda (dari main_webcame.py)
- **2**: Video - Tugas 1-4 lengkap (dari main_video.py)
- **3**: Gambar - Deteksi bouy di gambar (dari main_image.py)
- **4**: Keluar dari program

### 2. Webcam (main_webcame.py)

Deteksi semua benda secara real-time menggunakan webcam:
```
python main_webcame.py
```

- Tekan `q` untuk keluar.

### 3. Video (main_video.py)

Deteksi bouy dan obstacle di video, beserta tugas 1-4:
```
python main_video.py
```

Catatan: Pastikan file video `Edit Perjalanan Kapal (1).mp4` ada di folder `models/`.

- Tekan `q` untuk keluar.

### 4. Gambar (main_image.py)

Deteksi bouy dan obstacle di gambar, beserta tugas 1-4:
1. Masukkan gambar-gambar bouy ke folder `assets/`.
2. Jalankan program:
   ```
   python main_image.py
   ```
3. Tekan tombol apapun untuk lanjut ke gambar berikutnya.
4. Hasil deteksi akan disimpan di folder `assets/` dengan nama `output_nama_file.jpg`.

## Dependensi

Lihat file `requirements.txt` untuk daftar lengkap dependensi yang dibutuhkan.

## Catatan Penting

- Pastikan model `bola.pt` dan `yolov8n.pt` ada di folder proyek.
- Untuk video, pastikan file video `Edit Perjalanan Kapal (1).mp4` ada di folder `models/`.
- Untuk gambar, masukkan gambar-gambar bouy ke folder `assets/`.

## Lisensi

Proyek ini dibuat untuk keperluan pendidikan di RoboCamp.
