import aspose.slides as slides
import aspose.pydrawing as drawing
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\jayeshkumar.patel\Tesseract-OCR\tesseract.exe'

pres = slides.Presentation("C:\\Users\\jayeshkumar.patel\\Downloads\\New folder\\Quiz_120question.pptx")
filenew = open("C:\\Users\\jayeshkumar.patel\\Downloads\\New folder\\Quiz_Combined_TEST.txt", "a")
for sld in pres.slides:
    bmp = sld.get_thumbnail(1, 1)
    test = bmp.save("C:\\Users\\jayeshkumar.patel\\Downloads\\New folder\\Slide_{num}.jpg".format(num=str(sld.slide_number)), drawing.imaging.ImageFormat.jpeg)
    num=str(sld.slide_number)
    print(num)
    print("C:\\Users\\jayeshkumar.patel\\Downloads\\New folder\\Slide_" + num + ".jpg")
    f = ("C:\\Users\\jayeshkumar.patel\\Downloads\\New folder\\Slide_" + num + ".jpg")
    filenew.write('\n' + pytesseract.image_to_string(f))