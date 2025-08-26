import pytesseract
import os
directory = 'files'
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\jayeshkumar.patel\Tesseract-OCR\tesseract.exe'

print(pytesseract.image_to_string(r'C:\Users\jayeshkumar.patel\Downloads\Question Answer\p1gqavlijgslsogt10c68j6ntl4-1.jpg'))