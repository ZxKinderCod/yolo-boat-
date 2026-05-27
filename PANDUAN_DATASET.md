# Panduan Menyiapkan Dataset untuk Training YOLO

## Struktur Folder Dataset:
```
robocamp_for_student/
└── dataset/
    ├── images/
    │   ├── train/      # Tempatkan gambar untuk training (80% dari total gambar)
    │   └── val/        # Tempatkan gambar untuk validasi (20% dari total gambar)
    └── labels/
        ├── train/      # Tempatkan file label untuk training
        └── val/        # Tempatkan file label untuk validasi
```

## Langkah 1: Kumpulkan Gambar
1. Ambil foto-foto objek:
   - Bouy merah
   - Bouy hijau
   - Obstacle

## Langkah 2: Label Gambar
Gunakan tools label seperti:
- **LabelImg**: https://github.com/HumanSignal/labelImg
- **Roboflow**: https://roboflow.com (online, lebih mudah)
- **CVAT**: https://github.com/opencv/cvat

Saat labeling:
1. Buka gambar di tools labeling
2. Buat bounding box pada setiap objek
3. Beri label sesuai kelas:
   - `bouy_merah`
   - `bouy_hijau`
   - `obstacle`
4. Simpan label dalam format **YOLO** (.txt)

Format file label YOLO:
```
<class_id> <x_center> <y_center> <width> <height>
```
Contoh:
```
0 0.5 0.5 0.2 0.3
1 0.3 0.7 0.1 0.15
```

## Langkah 3: Susun File
- **80% gambar ke `dataset/images/train/`
- **20% gambar ke `dataset/images/val/`
- **File label (.txt) yang sesuai ke folder `dataset/labels/train/` dan `dataset/labels/val/`

Setiap gambar harus punya file label dengan nama yang SAMA (hanya ekstensi berbeda)!

Contoh:
- `gambar1.jpg` → `gambar1.txt`

## Langkah 4: Latih Model
Setelah dataset siap, jalankan script training!
