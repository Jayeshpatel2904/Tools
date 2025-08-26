f = open("C:\\Users\\jayeshkumar.patel\\Downloads\\Question Answer\\demofile2.txt", "a")
f.write('\n' + "Now the file has more content!")
f.close()

#open and read the file after the appending:
f = open("C:\\Users\\jayeshkumar.patel\\Downloads\\Question Answer\\demofile2.txt", "r")
print(f.read())