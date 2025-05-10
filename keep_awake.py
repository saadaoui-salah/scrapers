import pyautogui
import time


while True:
    # Simulate Ctrl+L key press
    #pyautogui.hotkey('ctrl', 'l')
    
    # Move mouse right and left
    pyautogui.move(100, 0, duration=0.5)
    pyautogui.move(-100, 0, duration=0.5)
    
    # Pause for a second
    time.sleep(5)