import os

script_dir = os.path.dirname(os.path.abspath(__file__))

try:
    from main_webcame import webcam_yolo_detection
except ImportError:
    print("File main_webcame.py tidak ditemukan!")
    webcam_yolo_detection = None

try:
    from main_video import video_buoy_detection
except ImportError:
    print("File main_video.py tidak ditemukan!")
    video_buoy_detection = None

try:
    from main_image import image_buoy_detection
except ImportError:
    print("File main_image.py tidak ditemukan!")
    image_buoy_detection = None

def main_menu():
    while True:
        print("          MENU UTAMA ROBOcamp")
        print("1. Webcam - Deteksi Semua   (dari main_webcame.py)")
        print("2. Video - (dari main_video.py)")
        print("3. Gambar - Deteksi Bouy di Gambar (dari main_image.py)")
        print("4. Keluar")
        choice = input("Pilih opsi (1-4): ").strip()
        if choice == "1":
            if webcam_yolo_detection:
                webcam_yolo_detection()
            else:
                print("ERROR: File main_webcame.py tidak ditemukan!")
        elif choice == "2":
            if video_buoy_detection:
                video_buoy_detection()
            else:
                print("ERROR: File main_video.py tidak ditemukan!")
        elif choice == "3":
            if image_buoy_detection:
                image_buoy_detection()
            else:
                print("ERROR: File main_image.py tidak ditemukan!")
        elif choice == "4":
            print("\nTerima kasih! Selamat tinggal!")
            break
        else:
            print("\nPilihan tidak valid!")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan. Selamat tinggal!")
