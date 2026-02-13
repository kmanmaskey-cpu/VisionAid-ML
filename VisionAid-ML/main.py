import cv2
import numpy as np
import winsound
import time

def get_entropy(roi):
    hist = cv2.calcHist([roi], [0], None, [256], [0, 256])
    hist = hist.ravel() / (hist.sum() + 1e-7)  # Probability Distribution P(x)
    hist = hist[hist > 0]  # Remove zero probabilities
    return -np.sum(hist * np.log2(hist))  # Shannon Entropy Formula

cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)

ret, first_frame = cap.read()
prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)

history = {"LEFT": [], "CENTER": [], "RIGHT": []}
last_beep_time = 0
is_calibrated = False
math = 0.15
counter = 0
last_heartbeat_time = 0

while True:
    ret, frame = cap.read()
    if not ret: 
        break  # to safe launch
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    
    avg_brightness = np.mean(gray) #1. Calculate Environmental Confidence
   
    low_light_mode = avg_brightness < 50    # If brightness < 50, the Canny filter will start seeing "noise"

    if low_light_mode:      # Play a low-frequency pulse to tell the user: "System is blind"
        
        if (time.time() - last_heartbeat_time > 1.0):     
            winsound.Beep(200, 100) # Low, sad beep
            last_heartbeat_time = time.time()
        continue    # Skip the rest of the logic for this frame to avoid false alarms



    h, w = gray.shape # h is length w i bredth

    flow = cv2.calcOpticalFlowFarneback(prev_gray[int(h*0.6):, :], gray[int(h*0.6):, :], None, 0.5, 3, 15, 3, 5, 1.2, 0)
    motion_mag = np.mean(np.sqrt(flow[...,0]**2 + flow[...,1]**2)) 
    expansion_multiplier = 1 + (motion_mag * 0.1)
    
    # Let's split the bottom of the screen into 3 Matrices: Left, Center, Right
    cell_w = w // 3
    floor_y = int(h * 0.6) # Only look at the bottom 40% of the screen (the floor)
    
    zones = {
        "LEFT": gray[floor_y:, 0:cell_w],
        "CENTER": gray[floor_y:, cell_w:2*cell_w],
        "RIGHT": gray[floor_y:, 2*cell_w:w]
    }
    
    for i, (name, area) in enumerate(zones.items()): # numerate teh zones 
        
        area = cv2.normalize(area, None, 0, 255, cv2.NORM_MINMAX) #stretches so it uses all 255 gray intensity levels 
        area = cv2.GaussianBlur(area, (5, 5), 0)
        area = cv2.Canny(area, 25, 75) #pixels<50 ignore and pixel>150 solid or ocnverts to 255
        kernel = np.ones((3,3), np.uint8)
        area = cv2.dilate(area, kernel, iterations=1)#connects hte dots and thicken the edges so it optimizes the canny
        
        if name == "CENTER":
            # Split CENTER into 3 horizontal slices: Top (Far), Mid, Bottom (Near)
            zh, zw = area.shape
            s = zh // 3
            far_slice  = area[0:s, :]
            mid_slice  = area[s:2*s, :]
            near_slice = area[2*s:zh, :]
            
            # Apply Perspective Weights: Near is 1.5x more important than Far
            base_entropy = (get_entropy(near_slice) * 1.5 + 
                           get_entropy(mid_slice) * 1.0 + 
                           get_entropy(far_slice) * 0.7) / 3.2
            entropy_val = base_entropy * expansion_multiplier
        else:
            entropy_val = get_entropy(area)
       
        color = (0, 255, 0) # green
        history[name].append(entropy_val)
        
        if is_calibrated:
            if len(history[name]) > 10:
                history[name].pop(0)
        else:   #takes 30 entropy smples then does the math on it
            if len(history['CENTER']) >= 30:
                math = np.mean(history['CENTER'][0:30]) + 2 * np.std(history['CENTER'][0:30])
                is_calibrated = True
        
        # AUDI0 TRIGGER: 
        if name == "CENTER": 
            avg = sum(history["CENTER"]) / (len(history["CENTER"]) + 1e-7)
            avg_left = sum(history["LEFT"]) / (len(history["LEFT"]) + 1e-7)
            avg_right = sum(history["RIGHT"]) / (len(history["RIGHT"]) + 1e-7)

            is_dangerous = avg > math
            

            if is_dangerous:
                counter = min(20, counter + 2)  # Increase danger counter
            else: 
                counter = max(0, counter - 1)  # Decrease counter when safe

            if counter >= 5:
                color = (0, 0, 255)    # turns red if high entropy 
                cv2.rectangle(frame, (cell_w, floor_y), (2*cell_w, h), color, 2) #makes a recntangular box 
                cv2.line(frame, (cell_w, floor_y + s), (2*cell_w, floor_y + s), (255, 255, 255), 2)
                cv2.line(frame, (cell_w, floor_y + 2*s), (2*cell_w, floor_y + 2*s), (255, 255, 255), 1)
                severity = avg - math
                # As severity goes up, the delay goes down (faster beeps)
                beep_delay = max(0.05, 0.5 - (severity * 2))
                pitch = 1200 if avg_left < avg_right else 400

                if (time.time() - last_beep_time > beep_delay):
                    #gives us a beep everytime the counter is above 5 and the pitch increases as the severity increases
                    winsound.Beep(int(pitch), 100)
                    last_beep_time = time.time()
                    
                    
            elif (time.time() - last_heartbeat_time > 2.0):
                winsound.Beep(150, 50) # Very low frequency, very short
                last_heartbeat_time = time.time()
            
        # Draw text
        cv2.putText(frame, f"{name}: {entropy_val:.2f}", (10 + (i*200), 50),  # shows text
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)


    prev_gray = gray.copy()  #updates memory for next frame              
    cv2.imshow("Synapse-Echo: Month 1 Spatial Test", frame) 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

cap.release() 
cv2.destroyAllWindows()