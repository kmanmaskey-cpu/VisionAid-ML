import cv2
import numpy as np
import winsound
import time

def get_entropy(roi):
    hist = cv2.calcHist([roi], [0], None, [256], [0, 256])
    hist = hist.ravel() / (hist.sum()+1e-7) # Probability Distribution P(x)
    hist = hist[hist > 0] # Remove zero probabilities
    return -np.sum(hist * np.log2(hist)) # Shannon Entropy Formula


cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
history = {"LEFT": [], "CENTER": [], "RIGHT": []}
last_beep_time = 0
is_calibrated = False
math = 0.15

while True:
    ret, frame = cap.read()
    if not ret: break  # to safe launch
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    h, w = gray.shape # h is length w i bredth
    
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
        area = cv2.Canny(area, 20, 100) #pixels<50 ignore and pixel>150 solid or ocnverts to 255
        
        entropy_val = get_entropy(area)
       
        color = (0, 255, 0) # green
        history[name].append(entropy_val)
        
        if is_calibrated :
            if len(history[name])> 10:
                    history[name].pop(0)
        else:
             math = np.mean(history['CENTER'][0:30])+2*np.std(history['CENTER'][0:30])
             is_calibrated= True
        
        # AUDI0 TRIGGER: I
        if name ==  "CENTER" :  

           
            
            avg = sum(history["CENTER"]) / (len(history["CENTER"]) + 1e-7)
            avg_left = sum(history["LEFT"]) / (len(history["LEFT"]) + 1e-7)
            avg_right = sum(history["RIGHT"]) / (len(history["RIGHT"]) + 1e-7)
            print(f"AVG: {avg:.4f}")

            is_dangerous = avg > math
            color = (0, 0, 255) if is_dangerous else (0, 255, 0)   # turns red if high entropy and green if its at optimal entropy
            cv2.rectangle(frame, (cell_w, floor_y), (2*cell_w, h), color, 2) #makes a recntangular box 
            
           
            if is_dangerous and (time.time() - last_beep_time > 1):
                
                    if avg_left<avg_right:
                        winsound.Beep(2000, 150)
                        last_beep_time = time.time()
                    elif avg_right<avg_left:
                        winsound.Beep(500,150)
                        last_beep_time = time.time()
                
        # Draw text
        cv2.putText(frame, f"{name}: {entropy_val:.2f}", (10 + (i*200), 50),  # shows text
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.imshow("Synapse-Echo: Month 1 Spatial Test", frame) #constnatly updating the video or using the for loop
    if cv2.waitKey(1) & 0xFF == ord('q'): break  # wait for 1 millisecond for image to process and q to quit

cap.release() # clena up crew .release , release the hardware attached to it
cv2.destroyAllWindows()# wipes ram
