import cv2
import numpy as np
import os

try:
    from ultralytics import YOLO
except ImportError:
    print("Package 'ultralytics' belum terinstal!")
    exit()

script_dir = os.path.dirname(os.path.abspath(__file__))

print("Loading model YOLOv8n untuk webcam...")
model_webcam = YOLO("yolov8n.pt")

def webcam_yolo_detection():
    print("\n=== WEBCAM - DETEKSI SEMUA BENDA ===")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Tidak bisa membuka webcam!")
        return
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    print("Webcam siap! Tekan 'q' untuk keluar.")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            results = model_webcam(frame, conf=0.3, imgsz=320, verbose=False)
            annotated_frame = results[0].plot()
            cv2.imshow("Webcam", annotated_frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or key == ord("Q"):
                break
    except KeyboardInterrupt:
        print("\nProgram dihentikan.")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Selesai dengan webcam.")

if __name__ == "__main__":
    try:
        webcam_yolo_detection()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan. Selamat tinggal!")
