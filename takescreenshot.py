import pygetwindow
import time
import os
import pyautogui
from PIL import Image


path = r'C:\Users\jayeshkumar.patel\Documents\Personal\Test\3\1.png'

titles = pygetwindow.getAllTitles

window = pygetwindow.getWindowsWithTitle('Command Prompt')[0]

left, top = window.topleft

right, bottom = window.bottomright

pyautogui.screenshot(path)

im = Image.open(path)

im = im.crop((left, top, right, bottom))

im.save(path)

im.show(path)

