import winsound
import time

print("Testing beeps...")

for i in range(3):
    winsound.Beep(1000 + i*500, 300)  # 1000 Hz → 1500 Hz → 2000 Hz
    time.sleep(0.5)

print("Beep test done.")