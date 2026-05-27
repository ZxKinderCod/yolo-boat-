import cv2
import numpy as np
import os
import time

try:
    from ultralytics import YOLO
except ImportError:
    print("Package 'ultralytics' belum terinstal!")
    exit()

script_dir = os.path.dirname(os.path.abspath(__file__))

model_video = None
model_path = os.path.join(script_dir, "bola.pt")
if os.path.exists(model_path):
    print("Loading model bola.pt untuk video...")
    model_video = YOLO(model_path)
else:
    print("Model bola.pt tidak ditemukan!")

def detect_color_obstacles(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_cyan1 = np.array([80, 80, 80])
    upper_cyan1 = np.array([110, 255, 255])
    lower_cyan2 = np.array([75, 70, 70])
    upper_cyan2 = np.array([115, 255, 255])
    mask_cyan1 = cv2.inRange(hsv, lower_cyan1, upper_cyan1)
    mask_cyan2 = cv2.inRange(hsv, lower_cyan2, upper_cyan2)
    mask_cyan = cv2.bitwise_or(mask_cyan1, mask_cyan2)
    
    lower_green_dark = np.array([35, 80, 80])
    upper_green_dark = np.array([75, 255, 255])
    mask_green_dark = cv2.inRange(hsv, lower_green_dark, upper_green_dark)
    
    mask = cv2.bitwise_or(mask_cyan, mask_green_dark)
    
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    obstacles = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 60000:
            x, y, w, h = cv2.boundingRect(cnt)
            ratio = float(w) / h
            if 0.3 <= ratio <= 3.0:
                obstacles.append((x, y, x+w, y+h, area))
    
    return obstacles

def video_buoy_detection():
    print("\n=== VIDEO - TUGAS 1-4 LENGKAP (DENGAN DETEKSI WARNA OBSTACLE) ===")
    if model_video is None:
        print("ERROR: Model bola.pt tidak diload!")
        return
    video_path = os.path.join(script_dir, "models", "Edit Perjalanan Kapal (1).mp4")
    if not os.path.exists(video_path):
        print(f"ERROR: File tidak ditemukan: {video_path}")
        return
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("ERROR: Tidak bisa membuka video!")
        return
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_center_x = frame_width // 2
    frame_center_y = frame_height // 2
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Resolusi: {frame_width}x{frame_height}")
    print(f"FPS: {fps:.1f}")
    print("Video siap! Tekan 'q' untuk keluar.")
    
    frame_count = 0
    last_red, last_green, last_obstacle = None, None, None
    prev_time = time.time()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            display = frame.copy()
            frame_count += 1
            
            current_time = time.time()
            fps_display = 1 / (current_time - prev_time) if (current_time - prev_time) > 0 else 0
            prev_time = current_time
            
            red, green, obstacle = None, None, None
            red_all, green_all, obstacle_all = [], [], []
            red_candidates = []
            green_candidates = []
            obstacle_candidates = []
            
            if frame_count % 1 == 0:
                results = model_video(frame, conf=0.2, imgsz=320, verbose=False)
                
                for result in results:
                    for box in result.boxes:
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
                        cls = int(box.cls[0].cpu().numpy())
                        conf = float(box.conf[0].cpu().numpy())
                        w, h = x2 - x1, y2 - y1
                        area, ratio = w * h, float(w) / h
                        
                        if cls == 1:
                            red_all.append((x1, y1, x2, y2, conf))
                            if 1000 <= area <= 40000 and 0.4 <= ratio <= 2.2:
                                red_candidates.append((x1, y1, x2, y2, area))
                        elif cls == 0:
                            if 1000 <= area <= 40000 and 0.4 <= ratio <= 2.2:
                                green_all.append((x1, y1, x2, y2, conf))
                                green_candidates.append((x1, y1, x2, y2, area))
                
                color_obstacles = detect_color_obstacles(frame)
                obstacle_candidates.extend(color_obstacles)
                
                if red_candidates:
                    red_candidates.sort(key=lambda x: x[4], reverse=True)
                    red = red_candidates[0][:4]
                    last_red = red
                
                if green_candidates:
                    green_candidates.sort(key=lambda x: x[4], reverse=True)
                    green = green_candidates[0][:4]
                    last_green = green
                
                if obstacle_candidates:
                    obstacle_candidates.sort(key=lambda x: x[4], reverse=True)
                    obstacle = obstacle_candidates[0][:4]
                    last_obstacle = obstacle
            
            r = red
            g = green
            o = obstacle if obstacle else last_obstacle
            
            for (x1, y1, x2, y2, conf) in red_all:
                cv2.rectangle(display, (x1, y1), (x2, y2), (0, 0, 255), 2)
                label = f"red {int(conf*100)}%"
                cv2.rectangle(display, (x1, y1-25), (x1+120, y1), (0, 0, 0), -1)
                cv2.putText(display, label, (x1+5, y1-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
            for (x1, y1, x2, y2, conf) in green_all:
                cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"green {int(conf*100)}%"
                cv2.rectangle(display, (x1, y1-25), (x1+130, y1), (0, 0, 0), -1)
                cv2.putText(display, label, (x1+5, y1-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            if o:
                cv2.rectangle(display, (o[0], o[1]), (o[2], o[3]), (255, 165, 0), 3)
                cv2.putText(display, "Obstacle", (o[0], o[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 165, 0), 2)
            
            decision = "STOP"
            avoidance = ""
            correction_m = 0
            mp = None
            rc, gc = None, None
            
            if r and g:
                rc = ((r[0]+r[2])//2, (r[1]+r[3])//2)
                gc = ((g[0]+g[2])//2, (g[1]+g[3])//2)
                mp = ((rc[0]+gc[0])//2, (rc[1]+gc[1])//2)
                
                cv2.line(display, (frame_center_x, frame_height), mp, (255, 255, 0), 2)
                cv2.line(display, rc, gc, (255, 255, 0), 2)
                cv2.circle(display, mp, 15, (255, 0, 0), -1)
                cv2.circle(display, mp, 8, (255, 255, 255), -1)
                cv2.putText(display, "MIDPOINT", (mp[0]+20, mp[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                
                obs_front = False
                obs_pos = ""
                if o:
                    oc = ((o[0]+o[2])//2, (o[1]+o[3])//2)
                    if oc[1] > frame_height * 0.3:
                        obs_front = True
                        if oc[0] < frame_center_x - 50:
                            obs_pos = "kiri"
                        elif oc[0] > frame_center_x + 50:
                            obs_pos = "kanan"
                        else:
                            obs_pos = "tengah"
                
                offset = mp[0] - frame_center_x
                correction_m = abs(offset) / 100.0
                
                if obs_front:
                    decision = "LEFT"
                    avoidance = "Ada Obstacle, ke Kiri"
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
            
            overlay = display.copy()
            cv2.rectangle(overlay, (10, 10), (280, 200), (50, 50, 50), -1)
            alpha = 0.7
            cv2.addWeighted(overlay, alpha, display, 1 - alpha, 0, display)
            
            cv2.putText(display, f"ARAH : {decision}", (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 255), 3)
            cv2.putText(display, f"Bouy Merah  : {len(red_all)}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.putText(display, f"Bouy Hijau  : {len(green_all)}", (20, 105), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            obs_count = 1 if o else 0
            cv2.putText(display, f"Obstacle     : {obs_count}", (20, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 165, 0), 2)
            cv2.putText(display, f"FPS : {fps_display:.1f}", (20, 155), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            if correction_m > 0 and r and g:
                koreksi_text = f"=> Koreksi {decision} {correction_m:.2f}m"
                cv2.putText(display, koreksi_text, (20, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            
            if r and g:
                bottom_overlay = display.copy()
                cv2.rectangle(bottom_overlay, (frame_width//2-300, frame_height-70), (frame_width//2+300, frame_height-20), (0, 0, 0), -1)
                alpha = 0.8
                cv2.addWeighted(bottom_overlay, alpha, display, 1 - alpha, 0, display)
                
                bottom_text = f"=> ARAHKAN KAPAL KE {decision} {correction_m:.2f} m"
                cv2.putText(display, bottom_text, (frame_width//2-280, frame_height-35), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 2)
            
            cv2.imshow("ASV Navigation System - RoboCamp 2026", display)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                break
                
    except KeyboardInterrupt:
        print("\nProgram dihentikan.")
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Selesai dengan video.")

if __name__ == "__main__":
    try:
        video_buoy_detection()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan. Selamat tinggal!")
