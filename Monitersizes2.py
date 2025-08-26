from PIL import ImageGrab
# ss_region = (3000, 300, 4000, 600)
# # ss_img = ImageGrab.grab(ss_region)
# ss_img = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True)
# ss_img.show()

# coding: utf-8
from datetime import datetime
from time import sleep

# from mss import mss


# with mss() as sct:
#     # while 'capturing':
#         filename = datetime.today().strftime(r"C:\Users\jayeshkumar.patel\Documents\Personal\Test\3\%Y%m%d_%H%M%S.png")
#         ss_img = sct.shot(mon=2)
#         print(ss_img)
#         ss_img.show()
#         sleep(1)

import mss.tools

with mss.mss() as sct:
    # Use the 1st monitor
    monitor = sct.monitors[1]

    # Capture a bbox using percent values
    left = monitor["left"] + monitor["width"] * 5 // 100 + 100 # 5% from the left
    top = monitor["top"] + monitor["height"] * 5 // 100  + 100 # 5% from the top
    right = left + 1900  # 400px width
    lower = top + 750  # 400px height
    bbox = (left, top, right, lower)

    # Grab the picture
    # Using PIL would be something like:
    # im = ImageGrab(bbox=bbox)
    im = sct.grab(bbox)

    filename = datetime.today().strftime(r"C:\Users\jayeshkumar.patel\Documents\Personal\Test\4\%Y%m%d_%H%M%S.png")
    print(datetime.today().strftime(r"%Y%m%d_%H%M%S"))
    mss.tools.to_png(im.rgb, im.size, output=filename)