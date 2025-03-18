import pyautogui
import time

while True:
    pyautogui.move(100, 0, duration=0.5)  # Move right
    pyautogui.move(-100, 0, duration=0.5)  # Move left
    time.sleep(1)  # Pause for a second