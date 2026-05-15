import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

# CONFIGURATION
# 0.01 seconds = ~100 clicks per second. Decrease to 0.001 for maximum speed.
DELAY = 0.1 
BUTTON = Button.left

# Change 'f4' to any key you prefer to turn it ON and OFF
TOGGLE_KEY = KeyCode(char='`') # Backtick key (usually next to the '1' key)

class AutoClicker(threading.Thread):
    def __init__(self, delay, button):
        super(AutoClicker, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        mouse = Controller()
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.1)

# Initialize and start the thread loop
click_thread = AutoClicker(DELAY, BUTTON)
click_thread.start()

def on_press(key):
    if key == TOGGLE_KEY:
        if click_thread.running:
            click_thread.stop_clicking()
            print("[INACTIVE] Auto-clicker paused.")
        else:
            click_thread.start_clicking()
            print("[ACTIVE] Auto-clicker spamming clicks...")

print("==================================================")
print(f"  PYNPUT HIGH-SPEED CLICKER (No-Sudo Required)   ")
print("==================================================")
print(f" Move mouse over target and press the [`] key to toggle.")
print(" Press Ctrl + C in this terminal window to close the script.")
print("==================================================")

try:
    with Listener(on_press=on_press) as listener:
        listener.join()
except KeyboardInterrupt:
    print("\nShutting down clicker...")
    click_thread.exit()
