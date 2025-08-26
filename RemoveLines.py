

directory = r'C:\Users\jayeshkumar.patel\Documents\Personal\Test\3.1'
filenew = open(directory + "\\Quiz_Combined_NEW_remove1.txt", "a")
with open(r'C:\Users\jayeshkumar.patel\Documents\Personal\Test\3.1\Quiz_Combined_NEW.txt','r+') as file:
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

