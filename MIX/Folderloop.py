import os
# assign directory
directory = r'C:\Users\jayeshkumar.patel\Documents\Personal\Test\4'
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\jayeshkumar.patel\Tesseract-OCR\tesseract.exe'
 
# iterate over files in
# that directory
filenew = open(directory + "\\Quiz_Combined_NEW.txt", "a")
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(f)
        # print(pytesseract.image_to_string(f))
        if "txt" not in f:
            filenew.write('\n' + pytesseract.image_to_string(f))

filenew.close()

filenew = open(directory + "\\Quiz_Combined_NEW_remove1.txt", "a")
with open(r'C:\Users\jayeshkumar.patel\Documents\Personal\Test\4\Quiz_Combined_NEW.txt','r+') as file:
    i = 1
    for line in file:

        if not line.isspace():
            if i == 0:

                if "Question" in line:
                    filenew.write("\n")
                    i = 1
                else:
                    filenew.write(line)
                    print(line)

            else: 
                if "Question" in line:
                    i = 0