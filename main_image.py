import cv2
import numpy as np
import os

try:
    from ultralytics import YOLO
except ImportError:
    print("Package 'ultralytics' belum terinstal!")
    exit()

script_dir = os.path.dirname(os.path.abspath(__file__))

model_video = None
model_path = os.path.join(script_dir, "bola.pt")
if os.path.exists(model_path):
    print("Loading model bola.pt untuk gambar...")
    model_video = YOLO(model_path)
else:
    print("Model bola.pt tidak ditemukan!")

def image_buoy_detection():
    print("\n=== GAMBAR - TUGAS 1-4 LENGKAP (FINAL) ===")
    if model_video is None:
        print("ERROR: Model bola.pt tidak diload!")
        return
    
    image_folder = os.path.join(script_dir, "assets")
    if not os.path.exists(image_folder):
        print(f"ERROR: Folder 'assets' tidak ditemukan di: {image_folder}")
        print("Silakan buat folder 'assets' dan masukkan gambar-gambar bouy!")
        return
    
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    if not image_files:
        print(f"ERROR: Tidak ada gambar di folder 'assets'!")
        print("Silakan masukkan gambar-gambar bouy ke folder 'assets'!")
        return
    
    print(f"Ditemukan {len(image_files)} gambar di folder 'assets'!")
    
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        print(f"\nMemproses: {image_file}")
        
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"ERROR: Tidak bisa membuka gambar: {image_file}")
            continue
        
        frame_height, frame_width = frame.shape[:2]
        frame_center_x = frame_width // 2
        display = frame.copy()
        
        red, green, obstacle = None, None, None
        red_candidates = []
        green_candidates = []
        obstacle_candidates = []
        
        results = model_video(frame, conf=0.3, imgsz=320, verbose=False)
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                cls = int(box.cls[0].cpu().numpy())
                w, h = x2 - x1, y2 - y1
                area, ratio = w * h, float(w) / h
                
                if cls == 1 and 1000 <= area <= 40000 and 0.4 <= ratio <= 2.2:
                    red_candidates.append((x1, y1, x2, y2, area))
                elif cls == 0:
                    if 1000 <= area <= 40000 and 0.4 <= ratio <= 2.2:
                        green_candidates.append((x1, y1, x2, y2, area))
                    elif area >= 60000 and 0.3 <= ratio <= 3.0:
                        obstacle_candidates.append((x1, y1, x2, y2, area))
        
        if red_candidates:
            red_candidates.sort(key=lambda x: x[4], reverse=True)
            red = red_candidates[0][:4]
        
        if green_candidates:
            green_candidates.sort(key=lambda x: x[4], reverse=True)
            green = green_candidates[0][:4]
        
        if obstacle_candidates:
            obstacle_candidates.sort(key=lambda x: x[4], reverse=True)
            obstacle = obstacle_candidates[0][:4]
        
        r = red
        g = green
        o = obstacle
        
        if r:
            cv2.rectangle(display, (r[0], r[1]), (r[2], r[3]), (0, 0, 255), 3)
            cv2.putText(display, "Bouy Merah", (r[0], r[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        if g:
            cv2.rectangle(display, (g[0], g[1]), (g[2], g[3]), (0, 255, 0), 3)
            cv2.putText(display, "Bouy Hijau", (g[0], g[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        if o:
            cv2.rectangle(display, (o[0], o[1]), (o[2], o[3]), (255, 165, 0), 3)
            cv2.putText(display, "Obstacle", (o[0], o[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2)
        
        decision = "STOP"
        avoidance = ""
        
        if r and g:
            rc = ((r[0]+r[2])//2, (r[1]+r[3])//2)
            gc = ((g[0]+g[2])//2, (g[1]+g[3])//2)
            mp = ((rc[0]+gc[0])//2, (rc[1]+gc[1])//2)
            cv2.line(display, rc, gc, (255, 255, 0), 2)
            cv2.circle(display, mp, 10, (255, 0, 0), -1)
            cv2.putText(display, "Midpoint", (mp[0]+15, mp[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
            
            obs_front = False
            obs_pos = ""
            if o:
                oc = ((o[0]+o[2])//2, (o[1]+o[3])//2)
                if oc[1] > frame_height * 0.5:
                    obs_front = True
                    if oc[0] < frame_center_x - 50:
                        obs_pos = "kiri"
                    elif oc[0] > frame_center_x + 50:
                        obs_pos = "kanan"
                    else:
                        obs_pos = "tengah"
            
            offset = mp[0] - frame_center_x
            
            if obs_front:
                if obs_pos == "kiri":
                    decision = "RIGHT"
                    avoidance = "Hindari Kanan"
                elif obs_pos == "kanan":
                    decision = "LEFT"
                    avoidance = "Hindari Kiri"
                else:
                    if offset < -30:
                        decision = "LEFT"
                    elif offset > 30:
                        decision = "RIGHT"
                    else:
                        decision = "FORWARD"
                    avoidance = "Pilih sisi aman"
            else:
                if offset < -30:
                    decision = "LEFT"
                elif offset > 30:
                    decision = "RIGHT"
                else:
                    decision = "FORWARD"
        
        d_color = (0, 0, 0)
        if decision == "LEFT":
            d_color = (255, 0, 0)
        elif decision == "RIGHT":
            d_color = (0, 0, 255)
        elif decision == "FORWARD":
            d_color = (0, 255, 0)
        
        cv2.rectangle(display, (10, 10), (200, 90), (255, 255, 255), -1)
        cv2.putText(display, decision, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, d_color, 2)
        
        if avoidance:
            cv2.rectangle(display, (10, 100), (200, 140), (255, 200, 200), -1)
            cv2.putText(display, avoidance, (20, 125), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        
        output_path = os.path.join(image_folder, f"output_{image_file}")
        cv2.imwrite(output_path, display)
        print(f"Hasil disimpan: {output_path}")
        
        cv2.imshow(f"Gambar - {image_file}", display)
        print("Tekan tombol apapun untuk lanjut ke gambar berikutnya...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    print("\nSelesai memproses semua gambar!")

if __name__ == "__main__":
    try:
        image_buoy_detection()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan. Selamat tinggal!")
