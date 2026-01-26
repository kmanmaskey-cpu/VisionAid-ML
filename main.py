import cv2
import numpy as np
import winsound
import time

def get_entropy(roi):
    # This is the math you learned in the ML specialization!
    hist = cv2.calcHist([roi], [0], None, [256], [0, 256])
    hist = hist.ravel() / (hist.sum()+1e-7) # Probability Distribution P(x)
    hist = hist[hist > 0] # Remove zero probabilities
    return -np.sum(hist * np.log2(hist)) # Shannon Entropy Formula

# Use your phone's IP camera URL from Grok's script
# cv2.CAP_DSHOW forces Python to use the Windows DirectShow driver
# We add + cv2.CAP_DSHOW to the index
cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW) # Or replace with your "http://..." URL
center_history = []
last_beep_time = 0


while True:
    ret, frame = cap.read()
    if not ret: break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    
    # Let's split the bottom of the screen into 3 Matrices: Left, Center, Right
    # This represents the path directly in front of the user
    cell_w = w // 3
    floor_y = int(h * 0.6) # Only look at the bottom 40% of the screen (the floor)
    
    zones = {
        "LEFT": gray[floor_y:, 0:cell_w],
        "CENTER": gray[floor_y:, cell_w:2*cell_w],
        "RIGHT": gray[floor_y:, 2*cell_w:w]
    }
    
    for i, (name, area) in enumerate(zones.items()):
        # A list to store the last few readings for the center
        
        area = cv2.Canny(area, 50, 150)
        area = cv2.normalize(area, None, 0, 255, cv2.NORM_MINMAX)
        entropy_val = get_entropy(area)
        # Determine safety
        color = (0, 255, 0)
        
        
        # AUDI0 TRIGGER: If the center path is blocked, make a noise!
        if name == "CENTER" :

            center_history.append(entropy_val)
            if len(center_history)> 10:
                center_history.pop(0)
            
            avg = sum(center_history)/len(center_history)

            is_dangerous = avg > 0.35
            color = (0, 0, 255) if is_dangerous else (0, 255, 0)
            cv2.rectangle(frame, (cell_w, floor_y), (2*cell_w, h), color, 2)
            
            # Frequency 1000Hz, Duration 100ms
            # Note: This will slightly slow down your FPS while it beeps
            if is_dangerous and (time.time() - last_beep_time > 1):
                winsound.Beep(1000, 150)
                last_beep_time = time.time()
        
        # Draw text
        cv2.putText(frame, f"{name}: {entropy_val:.2f}", (10 + (i*200), 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.imshow("Synapse-Echo: Month 1 Spatial Test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()