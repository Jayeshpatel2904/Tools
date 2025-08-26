# importing easygui module
from easygui import *
 
# message / information to be displayed on the screen
message = "Are you a Geek ?"
 
# title of the window
title = "GfG - EasyGUI"
 
# creating a yes no box
output = ynbox(message, title)
 
 
# if user pressed yes
if output:
     
    # message / information to be displayed on the screen
    message = "Thats Great !!"
  
    # title of the window
    title = "GfG - EasyGUI"
  
    # creating a message box
    msg = msgbox(message, title)
 
# if user pressed No
else:
     
    # message / information to be displayed on the screen
    message = "You should become a Geek, go to GeeksforGeeks to become one"
  
    # title of the window
    title = "GfG - EasyGUI"
  
    # creating a message box
    msg = msgbox(message, title)