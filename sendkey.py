import keyboard
from pynput.keyboard import Controller, Key
import time
import random

# Initialize the keyboard controller
keyboard_controller = Controller()

animal = ('1', '2', '3', '4')

# Wait for the initial Enter key press to start the loop
print("Press Enter to start...")
keyboard.wait('enter')  # This will start the loop when Enter is pressed once

# Now, the program will run the loop 500 times automatically
for _ in range(5):
   
    n = str(_)
    print(n)
    keyboard_controller.type(n)     # Writes "I love you"
    keyboard_controller.press(Key.enter)       # Presses the Enter key
    keyboard_controller.release(Key.enter)     # Releases the Enter key
    time.sleep(1)                            # Adds a short delay between iterations

# print("Finished writing 'I love you' 500 times.")
