import time
import datetime
now = datetime.datetime.now()
print (now.second)
 
# a module which has functions related to time.
# It can be installed using cmd command:
# pip install time, in the same way as pyautogui.
import pyautogui
import keyboard
keep_going = True
m = 0
time.sleep(4)
print(pyautogui.position())
while keep_going:
    now = datetime.datetime.now()
    s = now.second
    if keyboard.is_pressed("esc"):
        print("ending loop")
        keep_going = False
        break
    
    elif m != s:
        m = s
        i = 1
        print(s)

    elif (now.second == 59 and m == s and i == 1):
        i = 0
        print("Click")
        pyautogui.click(1867, 600)
    



